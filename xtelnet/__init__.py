import telnetlib,socket,re,threading,time

def escape_ansi(line):#this function escape all ANSI characters in any given string
    return  re.compile(r'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])').sub('',line.decode("utf-8"))

class session:
 def __init__(self):
  self.prompt=None
  self.telnet=None
 def get_banner(self,u,p=23,timeout=3):#this function is to grab banners only
  self.telnet = telnetlib.Telnet(u,p,timeout=timeout)
  m=self.telnet.expect([b'ser:',b'Name:',b'sername:',b'name:',b'ogin:',b'assword:',b'Pass:',b'pass:',b'nter>',b'asswd:'],timeout=timeout)#expected login prompts
  s=m[2]
  s=escape_ansi(s)
  self.telnet.close()
  self.telnet=None
  return "\r\n".join(s.split("\r\n")[:-1]).strip()
 def no_authentication(self,u,p=23,timeout=3):
  try:
   if self.telnet:
       raise Exception("Already connected")
   self.telnet = telnetlib.Telnet(u,p,timeout=timeout)
   c=''
   while True:
    s=escape_ansi(self.telnet.read_some())#expected login prompts
    c+=s.strip()
    if ((c[-1:]=='$') or (c[-1:]=='#') or (c[-1:]=='%') or (c[-1:]=='>') or (c[-1:]==']') ):#in case this is unauthenticated server
       self.prompt=(c.split("\r\n")[-1]).strip()
       c=None
       s=None
       break
  except socket.timeout:
   self.telnet=None
   raise Exception("Timed out")
 def authentication(self,u,username="",password="",p=23,timeout=3):
  try:
   usr=False
   if self.telnet:
       raise Exception("Already connected")
   self.telnet = telnetlib.Telnet(u,p,timeout=timeout)
   while True:
    m=self.telnet.expect([b'ser:',b'Name:',b'sername:',b'name:',b'ogin:',b'assword:',b'Pass:',b'pass:',b'nter>',b'asswd:'],timeout=timeout)#expected login prompts
    s=m[2]
    s=escape_ansi(s)
    if (('name:' in str(s).lower()) or ('login:' in str(s).lower()) or ('user:' in str(s).lower())):#in case it asked for username
     if usr==True:
        self.telnet.close()#close telnet connection
        self.telnet=None
        usr=None
        s=None
        c=None
        raise Exception("Authentication Failed")#so we don't get tricked into sending username multiple times after failure
     self.telnet.write("{}\n".format(username).encode('utf-8'))#send username
     usr=True
    elif (("password:" in str(s).lower()) or ("pass:" in str(s).lower()) or ("passwd:" in str(s).lower())):#in case it asked for password
     self.telnet.write("{}\n".format(password).encode('utf-8'))#send password
     break
    elif "enter>" in str(s).lower():
        self.telnet.write("\n".format(cmd.strip(),new_line).encode('utf-8'))#some anti-bot techniques requires sending "enter" after sending username/password
    else:
      c=s.strip()
      if ((c[-1:]=='$') or (c[-1:]=='#') or (c[-1:]=='%') or (c[-1:]=='>') or (c[-1:]==']') ):#in case this is unauthenticated server
       self.prompt=(c.split("\r\n")[-1]).strip()
       usr=None
       s=None
       c=None
       return None
      break
   usr=None
   while True:
      c=escape_ansi(self.telnet.read_some())#keep reading the data until we get the login result
      c=c.strip()
      if ('enter>' in c.lower()):
          self.telnet.write("\n".format(cmd.strip(),new_line).encode('utf-8'))
      else:
       if (('denied' in c.lower()) or ('bad' in c.lower()) or ("incorrect" in c.lower()) or ('failed' in c.lower()) or ('wrong' in c.lower()) or ('invalid' in c.lower()) or ('name:' in c.lower()) or ('login:' in c.lower()) or ('user:' in c.lower()) or ('password:' in c.lower()) or  ('pass:' in c.lower())):
          self.telnet.close()#close telnet connection
          self.telnet=None
          c=None
          raise Exception("Authentication Failed")#if login failed
       if ((c[-1:]=='$') or (c[-1:]=='#') or (c[-1:]=='%') or (c[-1:]=='>') or (c[-1:]==']') ):#in case authentication succeeded
        self.prompt=(c.split("\r\n")[-1]).strip()
        c=None
        return None
  except socket.timeout:
   self.telnet=None
   raise Exception("Timed out")
 def connect(self,u,username=None,password=None,p=23,timeout=3):#connect to a given host
  if (((username==None) or (username=="")) and ((password==None) or (password==""))):
    self.no_authentication(u,p=p,timeout=timeout)#for unauthenticated server
  else:
    self.authentication(u,p=p,timeout=timeout,username=username,password=password)#for authenticated server
 def execute(self,cmd,new_line='\n',timeout=2,more_timeout=2):#this function executes any command and returns the output
    if cmd!='':
      self.telnet.write("{} {}".format(cmd,new_line).encode('utf-8'))#send the command
      c=self.telnet.read_until("{}".format(self.prompt).encode('utf-8'),timeout=timeout)#read data until it receive the end of the prompt after executing the command
      if "---- More ----" in str(c):
         while True:#retrieve all commands 
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
    return c
 def interact(self):#this function start a direct interactive telnet session
     self.telnet.write("\n".encode('utf-8'))
     self.telnet.interact()
 def close(self):
     self.telnet.close()#close telnet connection
     self.telnet=None#free memory space
     self.prompt=None
 def logout(self,timeout=1):
     self.execute("logout",timeout=timeout)#logout of the telnet session
     self.close()#close telnet connection
 def exit(self,timeout=1):
     self.execute("exit",timeout=timeout)#exit the telnet session
     self.close()#close telnet connection
     
def dict_host(u,username=None,password=None,p=23,timeout=3):#this function takes those values and return a dict which contains all necessary information to create a telnet session using those following class
  return {"host":u,"username":username,"password":password,"port":p,"timeout":timeout}

class multi_session:#this class is made to control multiple sessions in parallel
 def __init__(self):
  self.sessions={}#a dict to save telnet sessions with this format: { ip : <telnet session object> }
  self.counter=None
 def connect(self,hosts,error_logs=False):#this function takes a list ("hosts" parameter) each element as a dict created by the function "dict_host" and use the information stored on it to create a session object for each ip
  self.counter=0
  for x in hosts:
    t=threading.Thread(target=self.connect_to_host,args=(x,error_logs,))#we are using threads to speed things up and connect to all hosts in a very short time (few seconds)
    t.start()
  while self.counter<len(hosts):
      time.sleep(.01)
  self.counter=None
 def connect_to_host(self,host,error):#connect to a single host it takes the "host_dict" 's returned value and save the ip and the session on the "self.sessions" variable 
  try:
   t=session()
   t.connect(host["host"],p=host["port"],timeout=host["timeout"],username=host["username"],password=host["password"])
   self.sessions.update({host["host"]:t})
  except Exception as e:
   if error==True:
    print("{} : {}".format(host["host"],str(e)))
  self.counter+=1
 def all_execute(self,cmd,timeout=2,error_logs=False):#execute the "cmd" on all hosts in "self.sessions"
  logs={}
  self.counter=0
  for x in self.sessions:
   t=threading.Thread(target=self.run_command,args=(x,cmd,timeout,logs,error_logs,))#again, we are using threads to speed thing up :)
   t.start()
  while self.counter<len(self.sessions):
      time.sleep(.01)
  self.counter=None
  return logs
 def some_execute(self,h,cmd,timeout=2,error_logs=False):#execute the "cmd" on some hosts in "self.sessions" whom are passed as a list ("h" parameter)
  logs={}
  self.counter=0
  for x in h:
   t=threading.Thread(target=self.run_command,args=(x,cmd,timeout,logs,error_logs,))
   t.start()
  while self.counter<len(h):
      time.sleep(.01)
  self.counter=None
  return logs
 def host_execute(self,h,cmd,timeout=2,error_logs=False):#execute the "cmd" on a single host in "self.sessions" which is passed as a string ("h" parameter)
  logs={}
  self.counter=0
  self.run_command(h,cmd,timeout,logs,error_logs)
  self.counter=None
  return logs
 def run_command(self,h,cmd,timeout,log,error):#execute the "cmd" on a single host which is passed as a string ("h" parameter)
  try:
   r=''
   t=self.sessions[h]
   r=t.execute(cmd,timeout=timeout)
  except Exception as e:
   if error==True:
    print("{} : {}".format(h,str(e)))
   r=str(e)
  log.update({h:{cmd:r}})
  self.counter+=1
 def disconnect_host(self,host):#disconnect from a single host, passed as string ("host" parameter), and remove it from "self.sessions"
     for x, v in list(self.sessions.items()):
         if x==host:
             self.sessions[x].close()
             del self.sessions[x]
 def disconnect_all(self):#disconnect from all hosts and remove them from "self.sessions"
     for x, v in list(self.sessions.items()):
             self.sessions[x].close()
             del self.sessions[x]
 def disconnect_some(self,h):#disconnect from some hosts, passed as list ("h" parameter), and remove them from "self.sessions"
    for x in h:
        self.disconnect_host(x)
