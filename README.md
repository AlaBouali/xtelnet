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
<br>t.login(ip, username='root',password='toor',p=23,timeout=5)
<br>output1=t.execute('echo ala_is_king')
<br>print(output1)
<br>output2=t.execute('cd / && ls')
<br>print(output2)
<br>t.close()

# Usage from command line :

<br>python -m xtelnet host [options...]

<br>options:


<br>--host : set a host to connect to (required)
<br>--username : set a username (required if username is needed to access)
<br>--password : set a password (required if password is needed to access)
<br>--port : (23 by default) set port (optional)
<br>--timeout : (5 by default) set timeout (optional)
<br>--add-command : a command to execute after login (optional)
<br>--command-timeout : timeout for command execution (optional)
<br>--set-newline : set a new line indecator("\n" or "\r\n") (optional)
<br>--no-shell : disable shell after authentication (optional)
<br>--help : get this help message (optional)

<br>example:

<br>python -m xtelnet 127.0.0.1 --username root --password root --add-command "echo ala" --add-command "dir"
