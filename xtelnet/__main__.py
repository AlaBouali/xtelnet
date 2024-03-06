import sys

if sys.version_info < (3, 0):
    input = raw_input
from .__init__ import *

c = sys.argv
user = ""
pwd = ""
host = ""
port = 23
timeout = 5
read_retries = 15
commands = []
new_line = "\n"
shell = True
usage = """

usage: xtelnet host [options...]

options:


-username : set a username (required if username is needed to access)
-password : set a password (required if password is needed to access)
-port : (23 by default) set port
-timeout : (5 by default) set timeout
--add-command : a command to execute after login and disable shell
--set-newline : ("\\n" by default) set a new line indecator("\\n" or "\\r\\n")
--no-shell : (enabled by default if no commands are specified) disable shell after authentication
--read-retries : times to retry reading the response if it takes too long
--help : get this help message

examples:

xtelnet 127.0.0.1 -username root -password root --add-command "echo ala" --add-command "dir"

xtelnet 127.0.0.1 -username root -password root -port 2323 -timeout 5

xtelnet 127.0.0.1 -username root -password root -port 2323 -timeout 5 --no-shell

"""
if len(c) < 2:
    print(usage)
    sys.exit()
host = c[1]
i = 0
while i < (len(c)):
    x = c[i]
    if x == "--help":
        print(usage)
        sys.exit()
    if x == "-port":
        port = int(c[i + 1])
        i += 1
    if x == "-timeout":
        timeout = int(c[i + 1])
        i += 1
    if x == "-username":
        user = c[i + 1]
        i += 1
    if x == "-password":
        pwd = c[i + 1]
        i += 1
    if x == "--read-retries":
        read_retries = int(c[i + 1])
        i += 1
    if x == "--no-shell":
        shell = False
    if x == "--add-command":
        commands.append(c[i + 1])
        i += 1
    if x == "--set-newline":
        command_timeout = c[i + 1]
        i += 1
    i += 1
if host == "":
    print("You need to set a host to connect to!!!")
    sys.exit()
if len(commands) > 0:
    shell = False


def run():
    t = Telnet_Session()
    try:
        t.connect(host, username=user, password=pwd, timeout=timeout, port=port,debug=True)
        if len(commands) > 0:
            for x in commands:
                t.execute(x)
            t.close()
        if shell == True:
            while True:
                cmd = input(t.prompt)
                if (
                    (cmd.lower().strip() == "exit")
                    or (cmd.lower().strip() == "logout")
                    or (cmd.lower().strip() == "quit")
                ):
                    t.close()
                    sys.exit()
                output = t.execute(cmd)
                if output == None:
                    output = ""
                if output != "":
                    print(output)
            t.close()
    except Exception as e:
        print("[-]Error: " + str(e))
