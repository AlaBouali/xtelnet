import telnetlib,socket,re
def escape_ansi(line):#this function escape all ANSI characters in any given string
    return  re.compile(r'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])').sub('',line.decode("utf-8"))
class session:
 def __init__(self):
  self.username=''
  self.password=''
  self.banner=''
  self.prompt=''
  self.prompt_end=b''
  self.telnet=None
  self.logs={}#where we save input and output logs
 def get_banner(self,u,p=23,timeout=3):#this function is to grab banners only
  self.telnet = telnetlib.Telnet(u,p,timeout=timeout)
  m=self.telnet.expect([b'ser:',b'Name:',b'sername:',b'name:',b'ogin:',b'assword:',b'Pass:',b'pass:',b'nter>'],timeout=timeout)#expected login prompts
  s=m[2]
  s=escape_ansi(s)
  self.telnet.close()
  return "\r\n".join(s.split("\r\n")[:-1]).strip()
 def login(self,u,username=None,password=None,p=23,timeout=3):
  try:
   usr=False
   pwd=False
   banner=False
   self.telnet = telnetlib.Telnet(u,p,timeout=timeout)
   while True:
    m=self.telnet.expect([b'ser:',b'Name:',b'sername:',b'name:',b'ogin:',b'assword:',b'Pass:',b'pass:',b'nter>'],timeout=timeout)#expected login prompts
    s=m[2]
    s=escape_ansi(s)
    if banner==False:
     self.banner="\r\n".join(s.split("\r\n")[:-1]).strip()
     banner=True
    if (('name:' in str(s).lower()) or ('login:' in str(s).lower()) or ('user:' in str(s).lower())):#in case it asked for username
     if usr==True:
        raise Exception("Authentication Failed")#so we don't get tricked into sending username multiple times after failure
     self.telnet.write("{}\n".format(username).encode('utf-8'))#send username
     usr=True
     self.username=username
    elif (("password:" in str(s).lower()) or ("pass:" in str(s).lower())):#in case it asked for password
     self.telnet.write("{}\n".format(password).encode('utf-8'))#send password
     pwd=True
     self.password=password
     break
    elif "enter>" in str(s).lower():
        self.telnet.write("\n".format(cmd.strip(),new_line).encode('utf-8'))#some anti-bot techniques requires sending "enter" after sending username/password
    else:
      c=s.strip()
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
      c=c.strip()
      if ('enter>' in c.lower()):
          self.telnet.write("\n".format(cmd.strip(),new_line).encode('utf-8'))
      else:
       if (('denied' in c.lower()) or ('bad' in c.lower()) or ("incorrect" in c.lower()) or ('failed' in c.lower()) or ('wrong' in c.lower()) or ('invalid' in c.lower()) or ('name:' in c.lower()) or ('login:' in c.lower()) or ('user:' in c.lower()) or ('password:' in c.lower()) or  ('pass:' in c.lower())):
          raise Exception("Authentication Failed")#if login failed
       if ((c[-1:]=='$') or (c[-1:]=='#') or (c[-1:]=='%') or (c[-1:]=='>') or (c[-1:]==']') ):#in case authentication succeeded
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
    if cmd!='':
      self.telnet.write("{} {}".format(cmd,new_line).encode('utf-8'))#send the command
      x=str(self.prompt)
      c=self.telnet.read_until("{}".format(self.prompt).encode('utf-8'),timeout=timeout)#read data until it receive the end of the prompt after executing the command
      if "---- More ----" in str(c):
         while True:
             self.telnet.write("\n".encode('utf-8'))
             o=self.telnet.read_until(b"---- More ----",timeout=more_timeout)
             if x.lower() in str(c).lower():
              break
             c+=o
      c=escape_ansi(c)
      c=c.strip()
      try:
       c=cmd.strip().join(c.split(cmd.strip())[1:]).strip()#remove the command sent from output
      except:
       pass
    else:#if the user just sending a new line
       self.telnet.write("\n".encode('utf-8'))
       c=escape_ansi(self.telnet.read_until("{}".format(self.prompt).encode('utf-8'),timeout=timeout)).strip()#read data until it receive the end of the prompt after executing the command
    try:
      self.prompt=(c.split("\r\n")[-1]).strip()#update telnet prompt when changing directory or terminal type
    except:
      pass
    try:
      c="\r\n".join(c.split("\r\n")[:-1])#remove the prompt from output
    except:
      pass
    self.logs.update({str(cmd.encode('utf-8')):str(c.encode('utf-8'))})#save the input and output into dict as logs
    return c
 def interact(self):#this function start a direct interactive telnet session
     self.telnet.write("\n".encode('utf-8'))
     self.telnet.interact()
 def close(self):
     self.telnet.close()#close telnet connection
 def logout(self,timeout=1):
     self.execute("logout",timeout=timeout)#logout of the telnet session
 def exit(self,timeout=1):
     self.execute("exit",timeout=timeout)#exit the telnet session
 def reset_session(self):
  self.username=''
  self.password=''
  self.banner=''
  self.prompt=''
  self.prompt_end=b''
  self.telnet=None
  self.logs={}
 def reset_username(self):
  self.username=''
 def reset_password(self):
  self.password=''
 def reset_banner(self):
  self.banner=''
 def reset_prompt(self):
  self.prompt=''
 def reset_prompt_end(self):
  self.prompt_end=b''
 def reset_logs(self):
  self.logs={}
 def reset_telnet(self):
  self.telnet=None
