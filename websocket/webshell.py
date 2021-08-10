import asyncio
import traceback

from websocket.ssh import Base
from websocket.connection import WebSocket


class WebShell(WebSocket):

    def __init__(self, scope, receive, send):
        super().__init__(scope, receive, send)
        self.ssh: Base = None

    def set_ssh(self, ssh):
        self.ssh = ssh

    async def ready(self):
        await self.accept()

    async def web_to_ssh(self):
        print('--------------->')
        try:

            while True:
                await asyncio.sleep(0.001)
                cmd = self.receive_text()
                print("cmd:", cmd)
                self.ssh.send(cmd)
        finally:
            self.clear()

    async def ssh_to_web(self):
        print('<-------------------')
        try:
            while True:
                await asyncio.sleep(0.001)
                data = self.ssh.read()
                if not data:
                    return
                await self.send_text(data)
                # print(self.cmd_string)
        finally:
            self.clear()

    async def run(self):
        if not self.ssh:
            raise Exception("ssh not init!")
        await asyncio.gather(
            self.web_to_ssh(),
            self.ssh_to_web()
        )

    def clear(self):
        try:
            self.close()
        except Exception:
            traceback.print_stack()
        try:
            self.ssh.close()
        except Exception:
            traceback.print_stack()
