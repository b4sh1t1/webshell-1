import asyncio
import traceback

from websocket.ssh import Base
from websocket.connection import WebSocket
import time
from .connection import WebSocket
from threading import Thread
import paramiko
import asyncio
from paramiko.channel import Channel


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



def get():
    """获取ssh登录的必须信息"""


async def echo(socket: WebSocket):
    """基础示例"""
    await socket.accept()
    while True:
        if not socket.status:
            return
        message = await socket.receive_text()
        print("send:", message)
        if not socket.status:
            return
        await socket.send_text(message)


async def webshell(web_session: WebSocket):
    await web_session.accept()
    print(web_session.query_string)
    print(web_session.query_params)
    print(web_session.path)
    ip, port, user, passwd = '10.57.19.239', 22, 'admin', 'qa@207'  # 定义全局变量连接信息.

    ip = web_session.query_params.get('ip') or ip
    port = web_session.query_params.get('port') or port
    user = web_session.query_params.get('user') or user
    passwd = web_session.query_params.get('passwd') or passwd

    ssh_session, msg = init_ssh(ip, port, user, passwd)
    await welcome(ssh_session, web_session)
    await asyncio.gather(
        web_to_ssh(ssh_session, web_session),
        ssh_to_web(ssh_session, web_session)
    )


async def welcome(ssh_session: Channel, web_session: WebSocket):
    # 展示Linux欢迎相关内容
    for i in range(2):
        if ssh_session.send_ready():
            message = ssh_session.recv(2048).decode('utf-8')
            if not message:
                return
            await web_session.send_text(message)


async def web_to_ssh(ssh_session: Channel, web_session: WebSocket):
    # print('--------web_to_ssh------->')
    while True:
        # print('--------------->')
        if not ssh_session.active or not web_session.status:
            return
        await asyncio.sleep(0.01)
        shell = await web_session.receive_text()
        # print('-------shell-------->', shell)
        if ssh_session.active and ssh_session.send_ready():
            ssh_session.send(bytes(shell, 'utf-8'))
        # print('--------------->', "end")


async def ssh_to_web(ssh_session: Channel, web_session: WebSocket):
    # print('<--------ssh_to_web-----------')
    while True:
        # print('<-------------------')
        if not ssh_session.active:
            await web_session.send_text('ssh closed')
            return
        if not web_session.status:
            return
        await asyncio.sleep(0.01)
        if ssh_session.recv_ready():
            message = ssh_session.recv(2048).decode('utf-8')
            # print('<---------message----------', message)
            if not len(message):
                continue
            await web_session.send_text(message)
        # print('<-------------------', "end")


def init_ssh(ip=None, port=None, user=None, passwd=None):
    # 如果是websocket连接就创建ssh连接，使用paramiko模块创建
    client = paramiko.SSHClient()  # 创建连接对象
    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy)  # 设置自动添加主机名及主机密钥到本地HostKeys对象，不依赖load_system_host_key的配置。即新建立ssh连接时不需要再输入yes或no进行确认
    try:  # 用异常抛出判定主机是否成功连接ssh
        client.connect(hostname=ip, port=port, username=user, password=passwd)  # connetc为连接函数
        print(f'主机{ip}连接成功！')
        msg = f'主机{ip}连接成功！'
    except:
        print(f'主机{ip}连接失败，请确认输入信息！')
        msg = f'主机{ip}连接失败！'

    ssh_session = client.get_transport().open_session()  # 成功连接后获取ssh通道
    # ssh_session.get_pty()  # 获取一个终端
    # 获取ssh通道，并设置term和终端大小
    ssh_session.get_pty(width=500, height=600)
    ssh_session.invoke_shell()  # 激活终端
    # 重设大小
    # ssh_session.resize_pty(width=500, height=600)
    return ssh_session, msg
