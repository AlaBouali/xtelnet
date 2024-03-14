import socks,socket,ssl,re,json
from .negotiations_flags import *

class Socket_Connection:

    @staticmethod
    def wrap_socket_with_ssl(sock,target_host):
        if sock==None:
            return
        if hasattr(ssl, 'PROTOCOL_TLS_CLIENT'):
            # Since Python 3.6
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        elif hasattr(ssl, 'PROTOCOL_TLS'):
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        else:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)#ssl.PROTOCOL_TLS)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context.wrap_socket(sock, server_hostname=target_host)
    
    @staticmethod
    def get_connection(host,port=23,proxy_host=None,proxy_port=None,proxy_type=None,username=None,password=None,timeout=5,use_ssl=False,**kwargs):
        try:
            s = socks.socksocket()
            s.settimeout(timeout)
            if proxy_type in [4,'s4','socks4'] :
                s.setproxy( 
                        proxy_type=socks.SOCKS4,
                        addr=proxy_host,
                        port=proxy_port,
                        username=username,
                        password=password,
                    )
            elif proxy_type in [5,'s5','socks5']:
                s.setproxy( 
                        proxy_type=socks.SOCKS5,
                        addr=proxy_host,
                        port=proxy_port,
                        username=username,
                        password=password,
                    )
            s.connect((host,port))
            if use_ssl==False:
                return s
            return Socket_Connection.wrap_socket_with_ssl(s,host)
        except:
            return
    
    @staticmethod
    def parse_for_negotiations(connection,received_data,debug=False):
        position=0
        negotiations_data=[Negotiation_Flags.IAC]
        for byte in received_data:
                #print(byte)
                # Check if it's a negotiation command
                if byte == ord(Negotiation_Flags.IAC) and received_data[position+1]!=ord(Negotiation_Flags.IAC):
                    command = received_data[position+1]
                    option = received_data[position+2]
                    if command not in negotiations_data:
                        negotiations_data.append(command)
                    if option not in negotiations_data:
                        negotiations_data.append(option)
                    Socket_Connection.handle_negotiation(connection, command, option,debug=debug)
                position+=1
        for x in negotiations_data:
            received_data=received_data.replace(x,'')
        return received_data
    
    @staticmethod
    def handle_negotiation(connection, command, option,debug=False):
        if debug==True:
            print('received negotiation: {} {}'.format(command,option))
        if command == ord(Negotiation_Flags.DO):
            # Server requests to enable an option
            connection.sendall("{}{}{}".format(Negotiation_Flags.IAC + Negotiation_Flags.IAC , Negotiation_Flags.WILL , option).encode())
            if debug==True:
                print("client negotiation response: {}{}{}".format(Negotiation_Flags.IAC + Negotiation_Flags.IAC , Negotiation_Flags.WILL , option))
        elif command == ord(Negotiation_Flags.DONT):
            # Server requests to disable an option
            connection.sendall("{}{}{}".format(Negotiation_Flags.IAC + Negotiation_Flags.IAC , Negotiation_Flags.WONT , option).encode())
            if debug==True:
                print("client negotiation response: {}{}{}".format(Negotiation_Flags.IAC + Negotiation_Flags.IAC , Negotiation_Flags.WONT , option))
        elif command == ord(Negotiation_Flags.WILL):
            # Server agrees to enable an option
            connection.sendall("{}{}{}".format(Negotiation_Flags.IAC + Negotiation_Flags.IAC , Negotiation_Flags.DO , option).encode())
            if debug==True:
                print("client negotiation response: {}{}{}".format(Negotiation_Flags.IAC + Negotiation_Flags.IAC , Negotiation_Flags.DO , option))
        elif command == ord(Negotiation_Flags.WONT):
            # Server refuses to enable an option
            connection.sendall("{}{}{}".format(Negotiation_Flags.IAC + Negotiation_Flags.IAC , Negotiation_Flags.DONT , option).encode())
            if debug==True:
                print("client negotiation response: {}{}{}".format(Negotiation_Flags.IAC + Negotiation_Flags.IAC , Negotiation_Flags.DONT , option))
        #else:
            #print('send nothing')

    @staticmethod
    def send_data(connection,data,timeout=5,debug=False,new_line="\n",enable_negotiation=False,**kwargs):
        if data!=None:
            if debug==True:
                    print("Sent: {}".format(Socket_Connection.escape_ansi(data)))
            connection.send("{}{}".format(data,new_line).encode())
        connection.settimeout(timeout)
        data=b''
        while True:
            try:
                d=connection.recv(4096)
                if debug==True:
                    print("received: {}".format(Socket_Connection.escape_ansi(d)))
                if d==b'':
                    break
                if enable_negotiation==True:
                    d=Socket_Connection.parse_for_negotiations(connection,d,debug=debug)
                data+=d
            except Exception as ex:
                #print(ex)
                break
        return Socket_Connection.escape_ansi(data)

    @staticmethod
    def destroy_connection(connection):
        connection.close()

    @staticmethod
    def escape_ansi(line):  # this function escape all ANSI characters in any given string
        if type(line) in [tuple,list,dict]:
            line=json.dumps(line)
        if type(line)==str:
            line=line.encode()
        return re.compile(
            r"(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
        ).sub("", line.decode("utf-8", "ignore")).strip()

    @staticmethod
    def get_banner(
    host, payload=None, **kwargs
):  # this function is to grab banners only
        sock=Socket_Connection.get_connection(host,**kwargs)
        data = Socket_Connection.send_data(sock,payload,**kwargs,)
        sock.close()
        return data

