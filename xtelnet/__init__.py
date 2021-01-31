import telnetlib,socket,re,threading,time

#if the default method didn't work out, then change the values inside those lists to reach your goal!!!

#expected login prompts ( don't forget the: "b" before the expected string )
login_prompts=[b'User:',b'user:',b'User>',b'user>',b'Name:',b'sername:',b'name:',b'Name>',b'sername>',b'name>',b'ogin:',b'ogin>',b'assword:',b'Pass:',b'pass:',b'nter>',b'asswd:',b'assword>',b'asswd>',b'pass>',b'Pass>']

#expected login failing prompts
fail_prompts=['expired','invalid','wrong','failed','incorrect','bad','denied','closed','user:','user>','username:','name:','username>','name>','login:','login>','password:','pass:','passwd:','password>','passwd>','pass>']

#expected username prompts
user_prompts=['user:','user>','username:','username>','name:','name>','login:','login>']

#expected password prompts
password_prompts=['password:','password>','pass:','pass>','passwd:','passwd>']

#expected anti-bot prompts
enter_prompts=['press return','press enter','enter>']

#expected ends of shell's prompt
prompt_end=['$','#','>','%',']']

def escape_ansi(line):#this function escape all ANSI characters in any given string
    return  re.compile(r'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])').sub('',line.decode("utf-8","ignore"))

def get_banner(u,p=23,timeout=3,payload=None):#this function is to grab banners only
  telnet = telnetlib.Telnet(u,p,timeout=timeout)
  if payload:
      telnet.write("{}".format(payload).encode('utf-8'))#in case we need to send any data to receive the banner
  c=''
  while True:
   try:
    s=escape_ansi(telnet.read_some())#keep reading data
    if s=='':
        break
    c+=s
   except:
       break
  telnet.close()
  telnet=None
  s=None
  return c.strip()

class session:
 
 __slots__=["prompt","prompt_before","telnet","connection_string","executing"]
 
 def __init__(self):
  self.prompt=None
  self.prompt_before=None
  self.telnet=None
  self.connection_string=None
  self.executing=None

 def no_authentication(self,u,p=23,timeout=3,debug_level=0):#just keep reading the data to the last byte, then we look for the prompt 
  try:
   if self.telnet:
       raise Exception("Already connected")
   self.telnet = telnetlib.Telnet(u,p,timeout=timeout)
   self.set_debug_level(debug_level)
   c=''
   while True:
    try:
     d=escape_ansi(self.telnet.read_some()).strip()
     c+=d
     if d=='':
         break
     if any(i in d.lower() for i in enter_prompts)==True:
        self.telnet.write("\n".encode('utf-8'))#some anti-bot techniques requires sending "enter" after sending username/password
    except:
        break
   d=None
   if (any(i in c.lower() for i in user_prompts)==False) and (any(i in c.lower() for i in password_prompts)==False):
     if (c[-1:] in prompt_end):#in case this is unauthenticated server
       self.prompt=(c.split("\r\n")[-1]).strip()
       c=None
     else:
       self.telnet.close()#close telnet connection
       self.telnet=None
       c=None
       raise Exception("Authentication Failed")
   else:
       self.telnet.close()#close telnet connection
       self.telnet=None
       c=None
       raise Exception("Authentication Failed")
  except socket.timeout:
   self.telnet=None
   raise Exception("Timed out")

 def authentication(self,u,username="",password="",p=23,timeout=3,debug_level=0):
  try:
   usr=False
   if self.telnet:
       raise Exception("Already connected")
   self.telnet = telnetlib.Telnet(u,p,timeout=timeout)
   self.set_debug_level(debug_level)
   while True:
    m=self.telnet.expect(login_prompts,timeout=timeout)#expected login prompts
    s=m[2]
    m=None
    s=escape_ansi(s)
    if any(i in s.lower() for i in user_prompts)==True:#in case it asked for username
     if "<myuser>" in s.lower():#cisco prompts can be tricky :) 1
         pass
     else: 
      if usr==True:
        self.telnet.close()#close telnet connection
        self.telnet=None
        usr=None
        s=None
        c=None
        raise Exception("Authentication Failed")#so we don't get tricked into sending username multiple times after failure
      self.telnet.write("{}\n".format(username).encode('utf-8'))#send username
      usr=True
    elif any(i in s.lower() for i in password_prompts)==True:#in case it asked for password
     if "<mypassword>" in s.lower():#cisco prompts can be tricky :) 2
         pass
     else:
      self.telnet.write("{}\n".format(password).encode('utf-8'))#send password
      break
    elif any(i in s.lower() for i in enter_prompts)==True:
        self.telnet.write("\n".encode('utf-8'))#some anti-bot techniques requires sending "enter" after sending username/password
    else:
      c=s.strip()
      if (c[-1:] in prompt_end):#in case this is unauthenticated server
       self.prompt=(c.split("\r\n")[-1]).strip()
       usr=None
       s=None
       c=None
       return None
   usr=None
   count=0
   while True:
      c=escape_ansi(self.telnet.read_some())#keep reading the data until we get the login result
      c=c.strip()
      if c=="":
          count+=1
          if count==3:
              self.telnet.close()#close telnet connection
              self.telnet=None
              c=None
              count=None
              raise Exception("Authentication Failed")#if login failed
      if any(i in str(c).lower() for i in enter_prompts)==True:
          self.telnet.write("\n".encode('utf-8'))
      else:
       if any(i in str(c).lower() for i in fail_prompts)==True:
          self.telnet.close()#close telnet connection
          self.telnet=None
          c=None
          count=None
          raise Exception("Authentication Failed")#if login failed
       if (c[-1:] in prompt_end):#in case authentication succeeded
        self.prompt=(c.split("\r\n")[-1]).strip()
        c=None
        count=None
        return None
  except socket.timeout:
   self.telnet=None
   raise Exception("Timed out")

 def connect(self,u,username=None,password=None,p=23,timeout=3,debug_level=0):#connect to a given host
  if (((username==None) or (username=="")) and ((password==None) or (password==""))):
    self.no_authentication(u,p=p,timeout=timeout,debug_level=debug_level)#for unauthenticated server
  else:
    self.authentication(u,p=p,timeout=timeout,username=username,password=password,debug_level=debug_level)#for authenticated server
  self.prompt_before=self.prompt
  self.connection_string="{}:{}:{}:{}".format(u,p,username,password)
  self.executing=False
  
 def reconnect(self,debug_level=0,timeout=3):#do reconnect if connection is lost and we didn't call "destroy" function of the object
  if self.telnet:
   self.close()
  l=self.connection_string.split(':')
  self.connect(l[0],p=int(l[1]),username=l[2],password=l[3],timeout=timeout,debug_level=debug_level)
  l=None

 def ping(self,new_line='\n'):#send empty string (new line) to keep the connection open: PING
  return self.execute('',new_line=new_line)

 def cwd(self,path,cmd='cd',new_line='\n',timeout=2):#change working directory
  while(self.executing!=False):
      time.sleep(0.1)
  self.executing=True
  cmd+=' '+path
  try:
   self.telnet.write("{} {}".format(cmd,new_line).encode('utf-8'))#send the command
   d=self.telnet.read_until("{}".format(self.prompt).encode('utf-8'),timeout=timeout).strip()#read data until it receive the end of the prompt after executing the command
   c=escape_ansi(d)
  except Exception as exc:
       self.executing=False
       raise Exception(exc)
  c=cmd.strip().join(c.split(cmd.strip())[1:]).strip()#remove the command sent from output
  self.executing=False
  try:
      self.prompt=(c.split("\r\n")[-1]).strip()#update telnet prompt when changing directory or terminal type
  except:
      pass
  try:
      c="\r\n".join(c.split("\r\n")[:-1])#remove the prompt from output
  except:
      pass
  self.executing=False
  return c.replace(self.prompt,'').strip()#remove the prompt from output if "?" has been used

 def switch_terminal(self,cmd,new_line='\n',timeout=2):#change terminal type
  while(self.executing!=False):
      time.sleep(0.1)
  self.executing=True
  try:
   self.telnet.write("{} {}".format(cmd,new_line).encode('utf-8'))#send the command
   d=self.telnet.read_until("{}".format(self.prompt).encode('utf-8'),timeout=timeout).strip()#read data until it receive the end of the prompt after executing the command
   c=escape_ansi(d)
   self.prompt=(c.split("\r\n")[-1]).strip()#update telnet prompt when changing directory or terminal type
  except Exception as exc:
       self.executing=False
       raise Exception(exc)
  self.executing=False
  c=cmd.strip().join(c.split(cmd.strip())[1:]).strip()#remove the command sent from output
  try:
      self.prompt=(c.split("\r\n")[-1]).strip()#update telnet prompt when changing directory or terminal type
  except:
      pass
  try:
      c="\r\n".join(c.split("\r\n")[:-1])#remove the prompt from output
  except:
      pass
  self.executing=False
  return c.replace(self.prompt,'').strip()#remove the prompt from output if "?" has been used

 def execute(self,cmd,new_line='\n',read_retries=15,wait_check=1):#this function executes any command and returns the output
    if self.prompt=='':
     self.prompt=self.prompt_before
    while(self.executing!=False):
      time.sleep(0.1)
    self.executing=True
    try:
     if cmd!='':
      c=''
      self.telnet.write("{} {}".format(cmd,new_line).encode('utf-8'))#send the command
      read_fails=0
      while True:
       more_end=False
       d=self.telnet.read_until("{}".format(self.prompt).encode('utf-8'),timeout=1).strip()#read data until it receive the end of the prompt after executing the command
       c+=escape_ansi(d)
       if str(self.prompt) in str(d):
        break
       if len(d)==0:
        read_fails+=1
       if read_fails==read_retries:
        break
       if "---- More ----" in str(d):
         while True:#retrieve all commands 
             self.telnet.write("{}".format(new_line).encode('utf-8'))
             o=self.telnet.read_until(b"---- More ----",timeout=1)
             d+=o
             if str(self.prompt) in str(o):
              more_end=True
              break
         o=None
         c+=escape_ansi(d)
         if more_end==True:
          break
      d=None
      more_end=None
      read_fails=None
      c=c.replace('---- More ----','').strip()
      if cmd.strip()!="?":
       try:
        c=cmd.strip().join(c.split(cmd.strip())[1:]).strip()#remove the command sent from output
       except:
        pass
     else:#if the user just sending a new line
       self.telnet.write("\n".encode('utf-8'))
       c=escape_ansi(self.telnet.read_until("{}".format(self.prompt).encode('utf-8'),timeout=2)).strip()#read data until it receive the end of the prompt after executing the command
    except Exception as exc:
       self.executing=False
       raise Exception(exc)
    try:
      self.prompt=(c.split("\r\n")[-1]).strip()#update telnet prompt when changing directory or terminal type
    except:
      pass
    try:
      c="\r\n".join(c.split("\r\n")[:-1])#remove the prompt from output
    except:
      pass
    self.executing=False
    c= c.replace(self.prompt,'').strip()#remove the prompt from output if "?" has been used
    if c.strip()=="" and cmd.strip()!="":
      while True:#for some reason after sending the command, the telnet receive the prompt without any content so we have to keep sending new lines with intervals until we receive the command's output
       try:
        time.sleep(wait_check)
        c=self.execute('',new_line=new_line)
        if c.strip()!="":
         break
       except Exception as exc:
        self.executing=False
        raise Exception(exc)
    return c

 def set_debug_level(self,level):
  self.telnet.debuglevel=level

 def interact(self):#this function start a direct interactive telnet session
     self.telnet.write("\n".encode('utf-8'))
     self.telnet.interact()

 def destroy(self):#close the connection and destroy the connection string 
     self.close()
     self.connection_string=None

 def close(self):
     self.telnet.close()#close telnet connection
     self.telnet=None
     self.prompt=None
     self.executing=None
     self.prompt_before=None

 def quit(self):
     self.execute("quit",read_retries=1)#logout of the telnet session
     self.close()#close telnet connection

 def logout(self):
     self.execute("logout",read_retries=1)#logout of the telnet session
     self.close()#close telnet connection

 def exit(self):
     self.execute("exit",read_retries=1)#exit the telnet session
     self.close()#close telnet connection
     




def dict_host(u,username=None,password=None,p=23,timeout=3):#this function takes those values and return a dict which contains all necessary information to create a telnet session using those following class
  return {"host":u,"username":username,"password":password,"port":p,"timeout":timeout}





class multi_session:#this class is made to control multiple sessions in parallel 

 __slots__=["sessions","counter","executing","connecting","executing"]

 def __init__(self):
  self.sessions={}#a dict to save telnet sessions with this format: { ip : <telnet session object> }
  self.counter=None
  self.executing=None
  self.connecting=False
  self.executing=False

 def connect(self,hosts,error_logs=False):#this function takes a list ("hosts" parameter) each element as a dict created by the function "dict_host" and use the information stored on it to create a session object for each ip
  while(self.connecting!=False):
   time.sleep(0.1)
  self.connecting=True
  self.counter=0
  if type(hosts)==dict:
   hosts=[hosts]
  for x in hosts:
    t=threading.Thread(target=self.connect_to_host,args=(x,error_logs,))#we are using threads to speed things up and connect to all hosts in a very short time (few seconds)
    t.start()
  while self.counter<len(hosts):
      time.sleep(.01)
  self.counter=None
  self.connecting=False

 def connect_to_host(self,host,error):#connect to a single host it takes the "host_dict" 's returned value and save the ip and the session on the "self.sessions" variable 
  try:
   t=session()
   t.connect(host["host"],p=int(host["port"]),timeout=int(host["timeout"]),username=host["username"],password=host["password"])
   self.sessions.update({host["host"]:t})
  except Exception as e:
   if error==True:
    print("{} : {}".format(host["host"],str(e)))
  self.counter+=1

 def ping(self,new_line='\n'):
  return self.all_execute('',new_line=new_line)

 def all_execute(self,cmd,read_retries=15,new_line='\n',error_logs=False):#execute the "cmd" on all hosts in "self.sessions"
  while(self.executing!=False):
   time.sleep(0.1)
  self.executing=True
  logs={}
  self.counter=0
  try:
   for x in self.sessions:
    t=threading.Thread(target=self.run_command,args=(x,cmd,read_retries,logs,error_logs,new_line,))#again, we are using threads to speed thing up :)
    t.start()
   while self.counter<len(self.sessions):
      time.sleep(.01)
   self.counter=None
   self.executing=False
   return logs
  except Exception as exc:
       self.executing=False
       raise Exception(exc)

 def some_execute(self,h,cmd,read_retries=15,new_line='\n',error_logs=False):#execute the "cmd" on some hosts in "self.sessions" whom are passed as a list ("h" parameter)
  while(self.executing!=False):
   time.sleep(0.1)
  self.executing=True
  logs={}
  self.counter=0
  try:
   for x in h:
    t=threading.Thread(target=self.run_command,args=(x,cmd,read_retries,logs,error_logs,new_line,))
    t.start()
   while self.counter<len(h):
      time.sleep(.01)
   self.counter=None
   self.executing=False
   return logs
  except Exception as exc:
       self.executing=False
       raise Exception(exc)

 def host_execute(self,h,cmd,read_retries=15,new_line='\n',error_logs=False):#execute the "cmd" on a single host in "self.sessions" which is passed as a string ("h" parameter)
  while(self.executing!=False):
   time.sleep(0.1)
  self.executing=True
  logs={}
  self.counter=0
  try:
   self.run_command(h,cmd,read_retries,logs,error_logs,new_line)
   self.counter=None
   self.executing=False
   return logs
  except Exception as exc:
       self.executing=False
       raise Exception(exc)

 def run_command(self,h,cmd,read_retries,log,error,newline):#execute the "cmd" on a single host which is passed as a string ("h" parameter)
  try:
   r=''
   t=self.sessions[h]
   r=t.execute(cmd,read_retries=read_retries,new_line=newline)
  except Exception as e:
   if error==True:
    print("{} : {}".format(h,str(e)))
   r=str(e)
  log.update({h:{cmd:r}})
  self.counter+=1

 def disconnect_host(self,host):#disconnect from a single host, passed as string ("host" parameter), and remove it from "self.sessions"
     for x, v in list(self.sessions.items()):
         if x==host:
             self.sessions[x].destroy()
             del self.sessions[x]

 def disconnect_all(self):#disconnect from all hosts and remove them from "self.sessions"
     for x, v in list(self.sessions.items()):
             self.sessions[x].destroy()
             del self.sessions[x]

 def disconnect_some(self,h):#disconnect from some hosts, passed as list ("h" parameter), and remove them from "self.sessions"
    for x in h:
        self.disconnect_host(x)

 def destroy(self):#destroy everything :) HAKAI !!!
    self.disconnect_all()
    self.sessions=None
    self.counter=None
    self.executing=None
    self.connecting=None
    self.executing=None