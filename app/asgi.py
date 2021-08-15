"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# asgi.py
import os
from django.core.asgi import get_asgi_application
from webshell.warp import warp as distribute_protocol

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_asgi_application()
application = distribute_protocol(application)

# 下面是极简版的实现,原理是相通的.
"""
async def application(scope, receive, send):
    if scope['type'] == 'http':
        await application(scope, receive, send)
    elif scope['type'] == 'webshell':
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")


async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event['type'] == 'webshell.connect':
            await send({
                'type': 'webshell.accept'
            })

        if event['type'] == 'webshell.disconnect':
            break

        if event['type'] == 'webshell.receive':
            if event['text'] == 'ping':
                await send({
                    'type': 'webshell.send',
                    'text': 'pong!'
                })
"""
