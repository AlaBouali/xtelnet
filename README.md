# xtelnet
This is an easy to use telnet module to interact with a remote system smoothly over this protocol!

# Install :

pip install xtelnet

or

pip3 install xtelnet

# Usage on a script :

import xtelnet
<br>t=xtelnet.session()
<br>ip='192.168.0.32'#just an example
<br>t.connect(ip, username='root',password='toor',p=23,timeout=5)
<br>output1=t.execute('echo ala_is_king')
<br>print(output1)
<br>output2=t.execute('cd / && ls')
<br>print(output2)
<br>t.close()



<h3>To start a manual interactive session after login, just do:</h3>


import xtelnet
<br>t=xtelnet.session()
<br>ip='192.168.0.32'#just an example
<br>t.connect(ip, username='root',password='toor',p=23,timeout=5)
<br>t.interact()



<h3>The multi_session helps you in controlling multiple telnet sessions in parallel:</h3>



import xtelnet
<br>t=xtelnet.multi_session()
<br>ip1='192.168.0.32'#just an example
<br>ip2='192.168.0.4'
<br>ip3='192.168.0.10'
<br>ip4='192.168.0.11'
<br>ip5='192.168.0.12'
<br>host1=xtelnet.dict_host(ip1, username='root',password='toor',p=23,timeout=5)
<br>host2=xtelnet.dict_host(ip2, username='root',password='toor',p=23,timeout=5)
<br>host3=xtelnet.dict_host(ip3, username='root',password='toor',p=23,timeout=5)
<br>host4=xtelnet.dict_host(ip4, username='root',password='toor',p=23,timeout=5)
<br>host5=xtelnet.dict_host(ip5, username='root',password='toor',p=23,timeout=5)
<br>t.connect([host1,host2,host3,host4,host5])
<br>print(t.sessions)#to see the connected hosts
<br>c=t.all_execute('echo "ala is king"')#execute this command on all hosts
<br>print(c)#print output
<br>c=t.some_execute([ip1,ip2],'echo "ala is king"')#execute this command on some hosts
<br>print(c)
<br>c=t.host_execute(ip1,'echo "ala is king"')#execute this command on this host
<br>print(c)
<br>t.disconnect_host(ip1)#to disconnect of this host
<br>t.disconnect_some([ip2,ip3])#to disconnect of those hosts
<br>t.disconnect_all()#to disconnect of all hosts




# Usage from command line :

<br>python -m xtelnet host [options...]

<br>options:


<br>-username : set a username (required if username is needed to access)
<br>-password : set a password (required if password is needed to access)
<br>-port : (23 by default) set port
<br>-timeout : (5 by default) set timeout
<br>--add-command : a command to execute after login
<br>--command-timeout : timeout for command execution
<br>--set-newline : set a new line indecator("\n" or "\r\n")
<br>--no-shell : disable shell after authentication
<br>--help : get this help message

<br>examples:

<br>python -m xtelnet 127.0.0.1 -username root -password root --add-command "echo ala" --add-command "dir"

<br>python -m xtelnet 127.0.0.1 -username root -password root -port 2323 -timeout 5

<br>python -m xtelnet 127.0.0.1 -username root -password root -port 2323 -timeout 5 --no-shell



# Xtelnet can be used to grab banners:


import xtelnet
<br>telnet_banner=xtelnet.get_banner("localhost",p=23)#suppose you have telnet server running on that port
<br>
<br>http_banner=xtelnet.get_banner("www.google.com",p=80,payload="GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")#we send a http request as a payload to get the response
<br>
<br>ssh_banner=xtelnet.get_banner("localhost",p=22)


# Xtelnet can escape all ANSI characters :


import xtelnet
<br>escaped_string=xtelnet.escape_ansi( unescaped_string )