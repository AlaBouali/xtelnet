import telnetlib,socket,re
def escape_ansi(line):
    return  re.compile(r'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])').sub('',line.decode("utf-8"))
class session:
 def __init__(self):
  self.prompt=''
  self.prompt_end=b''
  self.telnet=None
  self.logs={}#where we save input and output logs
 def login(self,u,username=None,password=None,p=23,timeout=3):
  try:
   usr=False
   pwd=False
   self.telnet = telnetlib.Telnet(u,p,timeout=timeout)
   while True:
    m=self.telnet.expect([b'ser:',b'Name:',b'sername:',b'name:',b'ogin:',b'assword:',b'Pass:',b'pass:',b'nter>'],timeout=timeout)#expected login prompts
    s=m[2]
    s=escape_ansi(s)
    if (('name:' in str(s).lower()) or ('login:' in str(s).lower()) or ('user:' in str(s).lower())):#in case it asked for username
     if usr==True:
        raise Exception("Authentication Failed")#so we don't get tricked into sending username multiple times after failure
     self.telnet.write("{}\n".format(username).encode('utf-8'))#send username
     usr=True
    elif (("password:" in str(s).lower()) or ("pass:" in str(s).lower())):#in case it asked for password
     self.telnet.write("{}\n".format(password).encode('utf-8'))#send password
     pwd=True
     break
    elif "enter>" in str(s).lower():
        self.telnet.write("\n".format(cmd.strip(),new_line).encode('utf-8'))#some anti-bot techniques requires sending "enter" after sending username/password
    else:
      c=str(s).lower()
      c=c.replace("b'",'')
      c=c.replace("'",'')
      c=c.replace('b"','')
      c=c.replace('"','')
      c=c.strip()
      if ((c[-1:]=='$') or (c[-1:]=='#') or (c[-1:]=='%') or (c[-1:]=='>') or (c[-1:]==']') ):#in case this is unauthenticated server
       self.prompt=(c.split("\r\n")[-1]).strip()
       if (c[-1:]=='$'):
           self.prompt_end=b'$'
       if (c[-1:]=='>'):
           self.prompt_end=b'>'
       if (c[-1:]=='#'):
           self.prompt_end=b'#'
       if (c[-1:]=='%'):
           self.prompt_end=b'%'
       if (c[-1:]==']'):
           self.prompt_end=b']'
       return None
      break
   while True:
      c=escape_ansi(self.telnet.read_some())#keep reading the data till get the login result
      c=c.replace("b'",'')
      c=c.replace("'",'')
      c=c.replace('b"','')
      c=c.replace('"','')
      c=c.strip()
      if ('enter>' in c):
          self.telnet.write("\n".format(cmd.strip(),new_line).encode('utf-8'))
      else:
       if (('denied' in c) or ('bad' in c) or ("incorrect" in c) or ('failed' in c) or ('wrong' in c) or ('invalid' in c) or ('name:' in c) or ('login:' in c) or ('user:' in c) or ('password:' in c) or  ('pass:' in c)):
          raise Exception("Authentication Failed")#if login failed
       if ((c[-1:]=='$') or (c[-1:]=='#') or (c[-1:]=='%') or (c[-1:]=='>') or (c[-1:]==']') ):#in case this is unauthenticated server
        self.prompt=(c.split("\r\n")[-1]).strip()
        if (c[-1:]=='$'):
           self.prompt_end=b'$'
        if (c[-1:]=='>'):
           self.prompt_end=b'>'
        if (c[-1:]=='#'):
           self.prompt_end=b'#'
        if (c[-1:]=='%'):
           self.prompt_end=b'%'
        if (c[-1:]==']'):
           self.prompt_end=b']'
        return None
  except socket.timeout:
   raise Exception("Timed out")
 def execute(self,cmd,new_line='\n',timeout=2,more_timeout=2):#this function executes any command and returns the output
    if cmd.strip()!='':
     self.telnet.write("{} {}".format(cmd.strip(),new_line).encode('utf-8'))#send the command
     x=str(self.prompt)
     c=self.telnet.read_until("{}".format(self.prompt).encode('utf-8'),timeout=timeout)#read data until it receive the end of the prompt after executing the command
     if "---- More ----" in str(c):
         while True:
             self.telnet.write("\n".format(cmd.strip(),new_line).encode('utf-8'))
             o=self.telnet.read_until(b"---- More ----",timeout=more_timeout)
             if x.lower() in str(c).lower():
              break
             c+=o
     c=escape_ansi(c)
     c=c.replace("b'",'')
     c=c.replace("'",'')
     c=c.replace('b"','')
     c=c.replace('"','')
     c=c.strip()
     try:
      c=cmd.strip().join(c.split(cmd.strip())[1:]).strip()#remove the command sent from output
     except:
      pass
     try:
      self.prompt=(c.split("\r\n")[-1]).strip()#update telnet prompt when changing directory or terminal type
     except:
      pass
     try:
      c="\r\n".join(c.split("\r\n")[:-1]).strip()#remove the prompt from output
     except:
      pass
     self.logs.update({str(cmd.strip()):str(c.strip())})#save the input and output into dict as logs
     return c.strip()
 def close(self):
     self.telnet.close()#close telnet connection
 def logout(self,timeout=1):
     self.execute("logout",timeout=timeout)#logout of the telnet session
 def exit(self,timeout=1):
     self.execute("exit",timeout=timeout)#exit the telnet session
