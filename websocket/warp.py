from django.urls import resolve
from websocket.connection import WebSocket


def warp(app):
    async def asgi(scope, receive, send):
        print("---debug---", scope, receive, send)
        if scope["type"] == "websocket":
            match = resolve(scope["raw_path"])
            await match.func(WebSocket(scope, receive, send), *match.args, **match.kwargs)
            return
        await app(scope, receive, send)

    return asgi
