import asyncio
from datetime import datetime
from django.views.generic.base import TemplateView
from webshell.webshell import WebShell, WebSocket


class IndexView(TemplateView):
    template_name = "index.html"


async def webshell_view(socket: WebSocket):
    socket = WebShell(socket)
    host, port, user, passwd = '192.168.186.77', 22, 'lgj', 'lgj123'
    socket.init_ssh(host, port, user, passwd)
    await socket.run()


async def time_view(socket: WebSocket):
    await socket.accept()
    while True:
        now = datetime.utcnow().isoformat() + "Z"
        if not socket.status:
            return
        await socket.send_text(now)
        await asyncio.sleep(0.01)


async def echo_view(socket: WebSocket):
    """基础示例"""
    await socket.accept()
    while True:
        if not socket.status:
            return
        await asyncio.sleep(0.01)
        message = await socket.receive_text()
        print("send:", message)
        if not socket.status:
            return
        await socket.send_text(message)
