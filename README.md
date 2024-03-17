# xtelnet
This is an easy to use telnet module to interact with a remote system smoothly over this protocol! It is a very minimalistic alterative to "telnetlib". xtelnet is a powerful and user-friendly Python library designed for managing Telnet sessions with ease and efficiency. With its intuitive interface and robust functionality, xtelnet simplifies the process of interacting with Telnet servers, offering a range of features for seamless communication. xtelnet offers a comprehensive solution for Telnet communication, providing developers with the tools they need to effectively manage Telnet sessions and interact with remote systems. Whether you're a seasoned developer or new to Telnet protocols, xtelnet empowers you to achieve your goals efficiently and reliably.

# Why should I use xtelnet?

<ul>
  <li>Easy to use and stable</li>
  <li>Simple Authentication mechanism</li>
  <li>Handle telnet negotiations automatically for you</li>
  <li>Compatible with python 2 and 3</li>
  <li>Set custom Telnet negotiation options</li>
  <li>parse commands output and returns only necessary output ( command's ouput, nothing extra )</li>
  <li>Compatible with almost all servers when it comes to authentication and executing the commands</li>
  <li>Available Command line tool</li>
  <li>Thread-safe: if the session is shared among threads to execute commands, the commands will be executed one by one</li>
  <li>Supports running multiple sessions concurrently</li>
  <li>Can connect simultaneously and run in parallel the same command on: single or some or all connected hosts</li>
  <li>Allow reconnect after closing the connection</li>
  <li>Allow escape ANSI characters</li>
  <li>Grab banners</li>
  <li>Available "ping" function to use if you want to keep the connection open</li>
  <li>Supports SOCKS 4 / 5 proxies</li>
  <li>Supports SSL</li>
  <li>Supports sending JSON data</li>
</ul>

# Install :

<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">pip install xtelnet
</pre></div>


or

<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">pip3 install xtelnet
</pre></div>


# Usage on a script :

<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">xtelnet</span>
t<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Telnet_Session()
ip<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.32&#39;</span><span style="color: #888888">#just an example</span>
# if you are using "stupid" tcp servers, just set "allow_raw_tcp" parameter in "connect" method to true and it will stream everything over TCP
t<span style="color: #333333">.</span>connect(ip, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,port<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
output1<span style="color: #333333">=</span>t<span style="color: #333333">.</span>execute(<span style="background-color: #fff0f0">&#39;echo ala_is_king&#39;</span>,timeout=5,buffer_read_timeout=2,remove_prompt_from_output=True,max_empty_buffers=3)
<span style="color: #008800; font-weight: bold">print</span>(output1)
output2<span style="color: #333333">=</span>t<span style="color: #333333">.</span>execute(<span style="background-color: #fff0f0">&#39;cd / &amp;&amp; ls&#39;</span>)
<span style="color: #008800; font-weight: bold">print</span>(output2)
output3<span style="color: #333333">=</span>t<span style="color: #333333">.</span>execute(<span style="background-color: #fff0f0">&#39;cd / &amp;&amp; ls&#39;</span>,read_until_match='expected_string_here')
<span style="color: #008800; font-weight: bold">print</span>(output3)
t<span style="color: #333333">.</span>close()<span style="color: #888888">#close the connection but keep the connection string to do reconnect later</span>
t<span style="color: #333333">.</span>enable_debug()<span style="color: #888888"># enable debug mode</span>
t<span style="color: #333333">.</span>disable_debug()<span style="color: #888888"># disable debug mode</span>
t<span style="color: #333333">.</span>reconnect()<span style="color: #888888">#reconnect to the host with the previous parameters</span>
t<span style="color: #333333">.</span>ping()<span style="color: #888888">#send new line to the host to keep the connectio open</span>
t<span style="color: #333333">.</span>destroy()<span style="color: #888888">#close the connection and remove the connection string totally, after this you can&#39;t do &quot;reconnect&quot;</span>
</pre></div>
<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">t.connect('114.35.81.134',proxy_type=5,proxy_host='localhost',proxy_port=9150,proxy_username='user',proxy_password='pass')#use SOCKS5 proxy to connect, set 'proxy_type' to 4 to use SOCKS4 
</pre></div>

<!--
<h3>To start a manual interactive session after login, just do:</h3>


<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">xtelnet</span>
t<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>session()
ip<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.32&#39;</span><span style="color: #888888">#just an example</span>
t<span style="color: #333333">.</span>connect(ip, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
t<span style="color: #333333">.</span>interact()
</pre></div>




-->
<h3>The multi_session helps you in controlling multiple telnet sessions in parallel:</h3>



<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">xtelnet</span>
t<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Multi_Telnet_Session()
ip1<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.32&#39;</span><span style="color: #888888">#just an example</span>
ip2<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.4&#39;</span>
ip3<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.10&#39;</span>
ip4<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.11&#39;</span>
ip5<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.12&#39;</span>
host1<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Telnet_Session.setup_host_configs(ip1, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,port<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
host2<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Telnet_Session.setup_host_configs(ip2, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,port<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
host3<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Telnet_Session.setup_host_configs(ip3, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,port<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
host4<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Telnet_Session.setup_host_configs(ip4, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,port<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
host5<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Telnet_Session.setup_host_configs(ip5, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,port<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
t<span style="color: #333333">.</span>connect([host1,host2,host3,host4,host5])
<span style="color: #008800; font-weight: bold">print</span>(t<span style="color: #333333">.</span>sessions)<span style="color: #888888">#to see the connected hosts</span>
c<span style="color: #333333">=</span>t<span style="color: #333333">.</span>all_execute(<span style="background-color: #fff0f0">&#39;echo &quot;ala is king&quot;&#39;</span>)<span style="color: #888888">#execute this command on all hosts</span>
<span style="color: #008800; font-weight: bold">print</span>(c)<span style="color: #888888">#print output</span>
c<span style="color: #333333">=</span>t<span style="color: #333333">.</span>some_execute([ip1,ip2],<span style="background-color: #fff0f0">&#39;echo &quot;ala is king&quot;&#39;</span>)<span style="color: #888888">#execute this command on some hosts</span>
<span style="color: #008800; font-weight: bold">print</span>(c)
c<span style="color: #333333">=</span>t<span style="color: #333333">.</span>host_execute(ip1,<span style="background-color: #fff0f0">&#39;echo &quot;ala is king&quot;&#39;</span>)<span style="color: #888888">#execute this command on this host</span>
<span style="color: #008800; font-weight: bold">print</span>(c)
t<span style="color: #333333">.</span>disconnect_host(ip1)<span style="color: #888888">#to disconnect of this host</span>
t<span style="color: #333333">.</span>disconnect_some([ip2,ip3])<span style="color: #888888">#to disconnect of those hosts</span>
t<span style="color: #333333">.</span>disconnect_all()<span style="color: #888888">#to disconnect of all hosts</span>
t<span style="color: #333333">.</span>destroy()<span style="color: #888888">#disconnect from all hosts</span>
</pre></div>





# Usage from command line :

<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%"><span style="color: #888888">xtelnet host [options...]</span>

<span style="color: #888888">options:</span>


<span style="color: #888888">-username : set a username (required if username is needed to access)</span>
<span style="color: #888888">-password : set a password (required if password is needed to access)</span>
<span style="color: #888888">-port : (23 by default) set port</span>
<span style="color: #888888">-timeout : (5 by default) set timeout</span>
<span style="color: #888888">--add-command : a command to execute after login and disable shell</span>
<span style="color: #888888">--set-newline : (&quot;\\n&quot; by default) set a new line indecator(&quot;\\n&quot; or &quot;\\r\\n&quot;)</span>
<span style="color: #888888">--no-shell : (enabled by default if no commands are specified) disable shell after authentication</span>
<span style="color: #888888">--read-retries : times to retry reading the response if it takes too long</span>
<span style="color: #888888">--help : get this help message</span>

<span style="color: #888888">examples:</span>

<span style="color: #888888">xtelnet 127.0.0.1 -username root -password root --add-command &quot;echo ala&quot; --add-command &quot;dir&quot;</span>

<span style="color: #888888">xtelnet 127.0.0.1 -username root -password root -port 2323 -timeout 5</span>

<span style="color: #888888">xtelnet 127.0.0.1 -username root -password root -port 2323 -timeout 5 --no-shell</span>
</pre></div>


# Xtelnet can be used to grab banners:


<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">xtelnet</span>
telnet_banner<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Socket_Connection.get_banner(<span style="background-color: #fff0f0">&quot;localhost&quot;</span>,port<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>)<span style="color: #888888">#suppose you have telnet server running on that port</span>

http_banner<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Socket_Connection.get_banner(<span style="background-color: #fff0f0">&quot;www.google.com&quot;</span>,port<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">80</span>,payload<span style="color: #333333">=</span><span style="background-color: #fff0f0">&quot;GET / HTTP/1.1</span><span style="color: #666666; font-weight: bold; background-color: #fff0f0">\r\n</span><span style="background-color: #fff0f0">Host: www.google.com</span><span style="color: #666666; font-weight: bold; background-color: #fff0f0">\r\n\r\n</span><span style="background-color: #fff0f0">&quot;</span>)<span style="color: #888888">#we send a http request as a payload to get the response</span>

ssh_banner<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Socket_Connection.get_banner(<span style="background-color: #fff0f0">&quot;localhost&quot;</span>,port<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">22</span>)
</pre></div>




# Xtelnet can escape all ANSI characters :


<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">xtelnet</span>
escaped_string<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>Socket_Connection.escape_ansi( unescaped_string )
</pre></div>

