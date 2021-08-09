from django.views.generic.base import TemplateView
from websocket.connection import WebSocket


class IndexView(TemplateView):
    template_name = "app/index.html"


async def websocket_view(socket: WebSocket):
    await socket.accept()
    while True:
        message = await socket.receive_text()
        print("send:", message)
        await socket.send_text(message)
