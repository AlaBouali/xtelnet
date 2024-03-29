from .socket_client import *
from .prompts import *
import sys,time

"""if sys.version_info < (3, 0):
    user_input=raw_input
else:
    user_input=input"""

class Telnet_Session:

    __slots__=['host','connection_configs','username','password','sock','debug','new_line','prompt','is_executing','is_connected','negotiation_options']

    """
    use this function to generate connection configs for hosts when usin multiple sessions
    """
    @staticmethod
    def setup_host_configs(
    host,login_timeout=60,timeout=3,username='',allow_raw_tcp=False,password='',new_line='\n', **kwargs
):  # this function takes those values and return a dict which contains all necessary information to create a telnet session using those following class
        kwargs.update({
        'host':host,
        'login_timeout':login_timeout,
        'timeout':timeout,
        'username':username,
        'password':password,
        'new_line':new_line,
        'allow_raw_tcp':allow_raw_tcp})
        return kwargs



    def __init__(self):
        self.host=None
        self.is_executing=None
        self.connection_configs=None
        self.username=None
        self.password=None
        self.new_line=None
        self.debug=None
        self.is_connected=None
        self.prompt=None
        self.sock=None
        self.negotiation_options={}

    def set_negotiation_option(self,option,command):
        if type(self.negotiation_options)!=dict:
            self.negotiation_options={}
        self.negotiation_options.update({option:command})

    # if you are using "stupid" tcp servers, just set "allow_raw_tcp" to true and it will stream everything over TCP
    def connect(self,host,login_timeout=60,timeout=3,negotiation_options={},username='',allow_raw_tcp=False,password='',new_line='\n',debug=False,enable_negotiation=False,**kwargs):
        if self.is_connected==True:
            raise Exception('Already connected to : {}'.format(host))
        self.host=host
        self.negotiation_options=negotiation_options
        self.connection_configs=kwargs
        self.username=username
        self.password=password
        self.new_line=new_line
        self.debug=debug
        self.is_executing=False
        self.prompt=None
        self.sock=Socket_Connection.get_connection(self.host,**kwargs)
        if self.sock==None:
            raise Exception('Failed to connect to : {}'.format(host))
        self.login(timeout=timeout,allow_raw_tcp=allow_raw_tcp,login_timeout=login_timeout,enable_negotiation=enable_negotiation)
    
    def login(self,timeout=5,allow_raw_tcp=False,login_timeout=60,enable_negotiation=False,**kwargs):
        self.is_connected=True
        login_started_at=time.time()
        username_sent=False
        password_sent=False
        data=Socket_Connection.send_data(self.sock,data=None,negotiation_options=self.negotiation_options,timeout=timeout,debug=self.debug,new_line=self.new_line,enable_negotiation=enable_negotiation).strip()
        prompt=data.split('\r\n')[-1] 
        empty_data_reads=0
        if allow_raw_tcp==True:
            return
        while True:
            if len(data)==0:
                empty_data_reads+=1
            if empty_data_reads==3:
                raise Exception("Authentication Failed")
            if time.time()-login_started_at>=login_timeout:
                self.destroy()
                raise Exception("Authentication Failed")
            if any(i in prompt.lower() for i in Telnet_Prompts.enter) == True:
                data=Socket_Connection.send_data(self.sock,data='',timeout=timeout,negotiation_options=self.negotiation_options,debug=self.debug,new_line='\r\n',enable_negotiation=enable_negotiation).strip()
                prompt=data.split('\r\n')[-1]
                # some anti-bot techniques requires sending "enter" after sending username/password
            if any(i in prompt.lower() for i in Telnet_Prompts.user) == True:
                if username_sent==True:
                    self.destroy()
                    raise Exception("Authentication Failed")
                data=Socket_Connection.send_data(self.sock,data=self.username,timeout=timeout,negotiation_options=self.negotiation_options,debug=self.debug,new_line=self.new_line,enable_negotiation=enable_negotiation).strip()
                prompt=data.split('\r\n')[-1]
                username_sent=True
            if any(i in prompt.lower() for i in Telnet_Prompts.password) == True:
                if password_sent==True:
                    self.destroy()
                    raise Exception("Authentication Failed")
                data=Socket_Connection.send_data(self.sock,data=self.password,timeout=timeout,negotiation_options=self.negotiation_options,debug=self.debug,new_line=self.new_line,enable_negotiation=enable_negotiation).strip()
                prompt=data.split('\r\n')[-1]
                password_sent=True
            if any(i in prompt.lower() for i in Telnet_Prompts.fail) == True:
                self.destroy()
                raise Exception("Authentication Failed")
            if (any(i in prompt.lower() for i in Telnet_Prompts.user) == False) and (
                any(i in prompt.lower() for i in Telnet_Prompts.password) == False
            ):
                if any(i in prompt.lower() for i in Telnet_Prompts.shell) == True:
                    self.prompt=prompt
                    return
                else:
                    self.destroy()
                    raise Exception("Authentication Failed")

    def execute(self,cmd,timeout=3,read_until_match=None,execution_is_done=True,buffer_read_timeout=2,remove_prompt_from_output=True,max_empty_buffers=1,enable_negotiation=False):
        """
        to put things in context:
            - cmd: the user's command
            - remove_prompt_from_output; return only the command's output without the prompts
            - timeout: initial command timeout, usually it will be enough. but sometimes it could take a bit longer than
            expected to get the full output, tha'st where the next parameter comes in hand
            - buffer_read_timeout: after getting the initial output we keep listening for any new coming data with a specific
            timeout for those read, hence 'buffer_read_timeout'
            - max_empty_buffers: how many expmty buffers to receive before exiting the loop and return the full output
        """
        while True:
            if self.is_executing==True:
                time.sleep(0.1)
            else:
                break
        self.is_executing=True
        if read_until_match!=None:
            self.just_execute(cmd)
            data = self.read_until(read_until_match,timeout=timeout)
            if execution_is_done==True:
                self.is_executing=False
            return data
        empty_buffers=0
        if max_empty_buffers<0:
            max_empty_buffers=0
        d=Socket_Connection.send_data(self.sock,cmd,timeout=timeout,negotiation_options=self.negotiation_options,new_line=self.new_line,debug=self.debug,enable_negotiation=enable_negotiation)
        data=d
        while True:
            if len(d)==0:
                empty_buffers+=1
            #print(d)
            if empty_buffers>=max_empty_buffers:
                break
            d=Socket_Connection.send_data(self.sock,data=None,negotiation_options=self.negotiation_options,timeout=buffer_read_timeout,new_line=self.new_line,debug=self.debug,enable_negotiation=enable_negotiation)
            data+=d
        self.is_executing=False
        if remove_prompt_from_output==False:
            return data
        self.prompt=data.split('\r\n')[-1]
        return '\r\n'.join(data.split('\r\n')[1:-1])
    
    def read_until(self,indicator,timeout=3):
        if type(indicator)==str:
            indicator=indicator.encode()
        self.sock.settimeout(timeout)
        data=b''
        while True:
            try:
                data+=self.sock.recv(1)
                if data.endswith(indicator)==True:
                    break
            except:
                break
        return data
    
    def just_execute(self,cmd):
        if type(cmd) in [list,tuple,dict]:
            cmd=json.dumps(cmd)
        if type(cmd)==bytes:
            cmd=cmd.decode()
        cmd+=self.new_line
        if type(cmd)==str:
            cmd=cmd.encode()
        self.sock.send(cmd)
    
    def ping(self):
        self.execute('')

    def close(self):
        self.sock.close()
        self.is_connected=False
        self.sock=None
    
    def enable_debug(self):
        self.debug=True
    
    def disable_debug(self):
        self.debug=False
    
    def destroy(self):
        self.host=None
        self.connection_configs=None
        self.username=None
        self.password=None
        self.is_connected=None
        self.negotiation_options=None
        try:
            self.sock.close()
        except:
            pass
        self.sock=None
        self.debug=None
        self.new_line=None
        self.prompt=None
    
    def quit(self):
        self.execute("quit", max_empty_buffers=0)  # logout of the telnet session
        self.close()  # close telnet connection

    def logout(self):
        self.execute("logout", max_empty_buffers=0)  # logout of the telnet session
        self.close()  # close telnet connection

    def exit(self):
        self.execute("exit", max_empty_buffers=0)  # exit the telnet session
        self.close()  # close telnet connection
    
    def reconnect(self,**kwargs):
        self.sock=Socket_Connection.get_connection(self.host,**kwargs)
        self.login(**kwargs)

    """def interact(self):
        cmd=user_input(self.prompt)
        Socket_Connection.send_data(self.sock,cmd,debug=True)
        #data=Telnet_Session.send_data(password,s,timeout=read_timeout,real_timeout=timeout,xor_key=xor_key)
        while True:
            cmd=user_input()
            self.execute(cmd)"""