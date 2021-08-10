import paramiko
import subprocess


class Base:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("NotImplementedError")

    def resize(self, cols, rows):
        raise NotImplementedError("NotImplementedError")

    def send(self, msg):
        raise NotImplementedError("NotImplementedError")

    def read(self, size=1024):
        raise NotImplementedError("NotImplementedError")

    def close(self):
        raise NotImplementedError("NotImplementedError")


class RemoteSSH(Base):

    def __init__(self, host, port, user, password=None, keyfile=None, passphrase=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.keyfile = keyfile
        self._ssh = paramiko.SSHClient()
        self._ssh.load_system_host_keys()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        k = keyfile and paramiko.RSAKey.from_private_key_file(keyfile, password=passphrase) or None
        self._ssh.connect(hostname=host, port=port, username=user, password=password, pkey=k)
        self._chanel = self._ssh.invoke_shell(term='xterm')

    def resize(self, cols, rows):
        self._chanel.resize_pty(width=cols, height=rows)

    def send(self, msg):
        self._chanel.send(msg)

    def read(self, size=1024):
        return self._chanel.recv(size)

    def close(self):
        self._chanel.close()


class LocalSSH(Base):
    def __init__(self):
        pass

    def read(self, size=1024):
        with subprocess.Popen(['sudo', 'python3', '-u', 'inline_print.py'], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, bufsize=0, universal_newlines=True) as p:
            for line in p.stdout:
                line = str(line.rstrip())
                await websocket.send(line)
                p.stdout.flush()
            for line in p.stderr:
                line = str(line.rstrip())
                await websocket.send(line)
                p.stdout.flush()
