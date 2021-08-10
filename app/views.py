import asyncio
from datetime import datetime
from django.views.generic.base import TemplateView
from websocket.webshell import WebShell, WebSocket
from websocket.ssh import RemoteSSH


class IndexView(TemplateView):
    template_name = "app/index.html"


async def webshell_view(socket: WebShell):
    ssh = RemoteSSH(123)
    socket.set_ssh(ssh)
    await socket.ready()
    await socket.run()


async def echo_view(socket: WebSocket):
    await socket.accept()
    while True:
        now = datetime.utcnow().isoformat() + "Z"
        await socket.send_text(now)
        await asyncio.sleep(1)
