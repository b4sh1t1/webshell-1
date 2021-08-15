__doc__ = "webshell主文件"

import asyncio
import traceback
import paramiko
from webshell.ssh import Base, RemoteSSH
from webshell.connection import WebSocket


class WebShell:
    """整理 WebSocket 和 paramiko.Channel,实现两者的数据互通"""

    def __init__(self, ws_session: WebSocket,
                 ssh_session: paramiko.SSHClient = None,
                 chanel_session: paramiko.Channel = None
                 ):
        self.ws_session = ws_session
        self.ssh_session = ssh_session
        self.chanel_session = chanel_session

    def init_ssh(self, host=None, port=22, user="admin", passwd="admin@123"):
        self.ssh_session, self.chanel_session = RemoteSSH(host, port, user, passwd).session()

    def set_ssh(self, ssh_session, chanel_session):
        self.ssh_session = ssh_session
        self.chanel_session = chanel_session

    async def ready(self):
        await self.ws_session.accept()

    async def welcome(self):
        # 展示Linux欢迎相关内容
        for i in range(2):
            if self.chanel_session.send_ready():
                message = self.chanel_session.recv(2048).decode('utf-8')
                if not message:
                    return
                await self.ws_session.send_text(message)

    async def web_to_ssh(self):
        # print('--------web_to_ssh------->')
        while True:
            # print('--------------->')
            if not self.chanel_session.active or not self.ws_session.status:
                return
            await asyncio.sleep(0.01)
            shell = await self.ws_session.receive_text()
            # print('-------shell-------->', shell)
            if self.chanel_session.active and self.chanel_session.send_ready():
                self.chanel_session.send(bytes(shell, 'utf-8'))
            # print('--------------->', "end")

    async def ssh_to_web(self):
        # print('<--------ssh_to_web-----------')
        while True:
            # print('<-------------------')
            if not self.chanel_session.active:
                await self.ws_session.send_text('ssh closed')
                return
            if not self.ws_session.status:
                return
            await asyncio.sleep(0.01)
            if self.chanel_session.recv_ready():
                message = self.chanel_session.recv(2048).decode('utf-8')
                # print('<---------message----------', message)
                if not len(message):
                    continue
                await self.ws_session.send_text(message)
            # print('<-------------------', "end")

    async def run(self):
        if not self.ssh_session:
            raise Exception("ssh not init!")
        await self.ready()
        await asyncio.gather(
            self.web_to_ssh(),
            self.ssh_to_web()
        )

    def clear(self):
        try:
            self.ws_session.close()
        except Exception:
            traceback.print_stack()
        try:
            self.ssh_session.close()
        except Exception:
            traceback.print_stack()
