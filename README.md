# xtelnet
This is an easy to use telnet module to interact with a remote system smoothly over this protocol!

# Install :

<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%">1</pre></td><td><pre style="margin: 0; line-height: 125%"><span style="color: #888888">pip install xtelnet</span>
</pre></td></tr></table></div>


or

<div style="background: #f8f8f8; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%">1</pre></td><td><pre style="margin: 0; line-height: 125%"><span style="color: #888888">pip3 install xtelnet</span>
</pre></td></tr></table></div>


# Usage on a script :

<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%"> 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15</pre></td><td><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">xtelnet</span>
t<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>session()
ip<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.32&#39;</span><span style="color: #888888">#just an example</span>
t<span style="color: #333333">.</span>connect(ip, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
output1<span style="color: #333333">=</span>t<span style="color: #333333">.</span>execute(<span style="background-color: #fff0f0">&#39;echo ala_is_king&#39;</span>)
<span style="color: #008800; font-weight: bold">print</span>(output1)
output2<span style="color: #333333">=</span>t<span style="color: #333333">.</span>execute(<span style="background-color: #fff0f0">&#39;cd / &amp;&amp; ls&#39;</span>)
<span style="color: #008800; font-weight: bold">print</span>(output2)
t<span style="color: #333333">.</span>cwd(<span style="background-color: #fff0f0">&#39;/&#39;</span>)<span style="color: #888888">#change working directory</span>
t<span style="color: #333333">.</span>switch_terminal(<span style="background-color: #fff0f0">&#39;tclsh&#39;</span>)<span style="color: #888888">#change terminal type where the prompt will get changed as well (just and example of command to do it on some routers)</span>
t<span style="color: #333333">.</span>switch_terminal(<span style="background-color: #fff0f0">&#39;tclquit&#39;</span>)
t<span style="color: #333333">.</span>close()<span style="color: #888888">#close the connection but keep the connection string to do reconnect later</span>
t<span style="color: #333333">.</span>reconnect()<span style="color: #888888">#reconnect to the host with the previous parameters</span>
t<span style="color: #333333">.</span>ping()<span style="color: #888888">#send new line to the host to keep the connectio open</span>
t<span style="color: #333333">.</span>destroy()<span style="color: #888888">#close the connection and remove the connection string totally, after this you can&#39;t do &quot;reconnect&quot;</span>
</pre></td></tr></table></div>



<h3>To start a manual interactive session after login, just do:</h3>


<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%">1
2
3
4
5</pre></td><td><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">xtelnet</span>
t<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>session()
ip<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.32&#39;</span><span style="color: #888888">#just an example</span>
t<span style="color: #333333">.</span>connect(ip, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
t<span style="color: #333333">.</span>interact()
</pre></td></tr></table></div>




<h3>The multi_session helps you in controlling multiple telnet sessions in parallel:</h3>



<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%"> 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24</pre></td><td><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">xtelnet</span>
t<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>multi_session()
ip1<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.32&#39;</span><span style="color: #888888">#just an example</span>
ip2<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.4&#39;</span>
ip3<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.10&#39;</span>
ip4<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.11&#39;</span>
ip5<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;192.168.0.12&#39;</span>
host1<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>dict_host(ip1, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
host2<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>dict_host(ip2, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
host3<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>dict_host(ip3, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
host4<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>dict_host(ip4, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
host5<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>dict_host(ip5, username<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;root&#39;</span>,password<span style="color: #333333">=</span><span style="background-color: #fff0f0">&#39;toor&#39;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>,timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">5</span>)
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
</pre></td></tr></table></div>




# Usage from command line :

<br>xtelnet host [options...]

<br>options:


<br>-username : set a username (required if username is needed to access)
<br>-password : set a password (required if password is needed to access)
<br>-port : (23 by default) set port
<br>-timeout : (5 by default) set timeout
<br>--add-command : a command to execute after login and disable shell
<br>--set-newline : ("\\n" by default) set a new line indecator("\\n" or "\\r\\n")
<br>--no-shell : (enabled by default if no commands are specified) disable shell after authentication
<br>--read-retries : times to retry reading the response if it takes too long
<br>--help : get this help message

<br>examples:

<br>xtelnet 127.0.0.1 -username root -password root --add-command "echo ala" --add-command "dir"

<br>xtelnet 127.0.0.1 -username root -password root -port 2323 -timeout 5

<br>xtelnet 127.0.0.1 -username root -password root -port 2323 -timeout 5 --no-shell



# Xtelnet can be used to grab banners:


<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%">1
2
3
4
5
6</pre></td><td><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">xtelnet</span>
telnet_banner<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>get_banner(<span style="background-color: #fff0f0">&quot;localhost&quot;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">23</span>)<span style="color: #888888">#suppose you have telnet server running on that port</span>

http_banner<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>get_banner(<span style="background-color: #fff0f0">&quot;www.google.com&quot;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">80</span>,payload<span style="color: #333333">=</span><span style="background-color: #fff0f0">&quot;GET / HTTP/1.1</span><span style="color: #666666; font-weight: bold; background-color: #fff0f0">\r\n</span><span style="background-color: #fff0f0">Host: www.google.com</span><span style="color: #666666; font-weight: bold; background-color: #fff0f0">\r\n\r\n</span><span style="background-color: #fff0f0">&quot;</span>)<span style="color: #888888">#we send a http request as a payload to get the response</span>

ssh_banner<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>get_banner(<span style="background-color: #fff0f0">&quot;localhost&quot;</span>,p<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">22</span>)
</pre></td></tr></table></div>



# Xtelnet can escape all ANSI characters :


<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%">1
2</pre></td><td><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">xtelnet</span>
escaped_string<span style="color: #333333">=</span>xtelnet<span style="color: #333333">.</span>escape_ansi( unescaped_string )
</pre></td></tr></table></div>
