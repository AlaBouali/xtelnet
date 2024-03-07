from .telnet_client import *
import threading


class Multi_Telnet_Session:  # this class is made to control multiple sessions in parallel

    __slots__ = ["sessions", "counter", "executing", "connecting"]

    def __init__(self):
        self.sessions = (
            {}
        )  # a dict to save telnet sessions with this format: { ip : <telnet session object> }
        self.counter = None
        self.connecting = False
        self.executing = False

    def connect(
        self, hosts, error_logs=False
    ):  # this function takes a list ("hosts" parameter) each element as a dict created by the function "Telnet_Session.setup_host_configs" and use the information stored on it to create a session object for each ip
        while self.connecting != False:
            time.sleep(0.1)
        self.connecting = True
        self.counter = 0
        if type(hosts) == dict:
            hosts = [hosts]
        for x in hosts:
            t = threading.Thread(
                target=self.connect_to_host,
                args=(
                    x,
                    error_logs,
                ),
            )  # we are using threads to speed things up and connect to all hosts in a very short time (few seconds)
            t.start()
        while self.counter < len(hosts):
            time.sleep(0.01)
        self.counter = None
        self.connecting = False

    def connect_to_host(
        self, host, error
    ):  # connect to a single host it takes the "Telnet_Session.setup_host_configs" 's returned value and save the ip and the session on the "self.sessions" variable
        try:
            t = Telnet_Session()
            t.connect(
                **host)
            self.sessions.update({host["host"]: t})
        except Exception as e:
            if error == True:
                print("{} : {}".format(host["host"], str(e)))
        self.counter += 1

    def ping(self, new_line="\n"):
        return self.all_execute("", new_line=new_line)

    def all_execute(
        self, cmd, error_logs=False,**kwargs
    ):  # execute the "cmd" on all hosts in "self.sessions"
        while self.executing != False:
            time.sleep(0.1)
        self.executing = True
        logs = {}
        self.counter = 0
        try:
            for x in self.sessions:
                t = threading.Thread(
                    target=self.run_command,
                    args=(
                        x,
                        cmd,
                        logs,
                        error_logs,
                        kwargs,
                    ),
                )  # again, we are using threads to speed thing up :)
                t.start()
            while self.counter < len(self.sessions):
                time.sleep(0.01)
            self.counter = None
            self.executing = False
            return logs
        except Exception as exc:
            self.executing = False
            raise Exception(exc)

    def some_execute(
        self, h, cmd, error_logs=False, **kwargs
    ):  # execute the "cmd" on some hosts in "self.sessions" whom are passed as a list ("h" parameter)
        while self.executing != False:
            time.sleep(0.1)
        self.executing = True
        logs = {}
        self.counter = 0
        try:
            for x in h:
                t = threading.Thread(
                    target=self.run_command,
                    args=(
                        x,
                        cmd,
                        logs,
                        error_logs,
                        kwargs,
                    ),
                )
                t.start()
            while self.counter < len(h):
                time.sleep(0.01)
            self.counter = None
            self.executing = False
            return logs
        except Exception as exc:
            self.executing = False
            raise Exception(exc)

    def host_execute(
        self, h, cmd, error_logs=False, **kwargs
    ):  # execute the "cmd" on a single host in "self.sessions" which is passed as a string ("h" parameter)
        while self.executing != False:
            time.sleep(0.1)
        self.executing = True
        logs = {}
        self.counter = 0
        try:
            self.run_command(h, cmd, logs, error_logs, kwargs)
            self.counter = None
            self.executing = False
            return logs
        except Exception as exc:
            self.executing = False
            raise Exception(exc)

    def run_command(self, h, cmd, logs, error_logs, kwargs):
        try:
            r = ""
            t = self.sessions[h]
            r = t.execute(cmd, **kwargs)
        except Exception as e:
            if error_logs:
                print("{} : {}".format(h, str(e)))
            r = str(e)
        logs.update({h: {cmd: r}})
        self.counter += 1


    def disconnect_host(
        self, host
    ):  # disconnect from a single host, passed as string ("host" parameter), and remove it from "self.sessions"
        for x, v in list(self.sessions.items()):
            if x == host:
                self.sessions[x].destroy()
                del self.sessions[x]

    def disconnect_all(
        self,
    ):  # disconnect from all hosts and remove them from "self.sessions"
        for x, v in list(self.sessions.items()):
            self.sessions[x].destroy()
            del self.sessions[x]

    def disconnect_some(
        self, h
    ):  # disconnect from some hosts, passed as list ("h" parameter), and remove them from "self.sessions"
        for x in h:
            self.disconnect_host(x)

    def destroy(self):  # destroy everything :) HAKAI !!!
        self.disconnect_all()
        self.sessions = None
        self.counter = None
        self.executing = None
        self.connecting = None
