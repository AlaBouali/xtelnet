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



<h3>To start a manual interactive session after login, just do:</h3>


import xtelnet
<br>t=xtelnet.session()
<br>ip='192.168.0.32'#just an example
<br>t.login(ip, username='root',password='toor',p=23,timeout=5)
<br>t.interact()



<h3>The session class contains all the data of the session (username, password, telnet's banner, prompt, prompt's end, session logs):</h3>



import xtelnet
<br>t=xtelnet.session()
<br>ip='192.168.0.32'#just an example
<br>t.login(ip, username='root',password='toor',p=23,timeout=5)
<br>t.execute('ls')
<br>print(t.username)
<br>print(t.password)
<br>print(t.banner)
<br>print(t.prompt)
<br>print(t.prompt_end)
<br>print(t.logs)



<h3>To reset the session's saved data:</h3>



import xtelnet
<br>t=xtelnet.session()
<br>ip='192.168.0.32'#just an example
<br>t.login(ip, username='root',password='toor',p=23,timeout=5)
<br>t.execute('ls')
<br>t.close()
<br>t.reset_session()


<h3>To get the telnet's banner of the remote machine:</h3>


<h4>(no login)</h4>

import xtelnet
<br>t=xtelnet.session()
<br>ip='192.168.0.32'#just an example
<br>banner=t.get_banner(ip,p=23,timeout=5)
<br>print(banner)



<h4>(after login)</h4>



import xtelnet
<br>t=xtelnet.session()
<br>ip='192.168.0.32'#just an example
<br>t.login(ip, username='root',password='toor',p=23,timeout=5)
<br>banner=t.banner
<br>print(banner)



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
