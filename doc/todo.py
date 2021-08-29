from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    MutableMapping,
    Optional,
    Union,
)

from httptools import HttpParserUpgrade  # type: ignore
from websockets import (  # type: ignore
    ConnectionClosed,
    InvalidHandshake,
    WebSocketCommonProtocol,
)

# Despite the "legacy" namespace, the primary maintainer of websockets
# committed to maintaining backwards-compatibility until 2026 and will
# consider extending it if sanic continues depending on this module.
from websockets.legacy import handshake

# from sanic.exceptions import InvalidUsage

__all__ = ["WebSocketProtocol", "WebSocketConnection"]

ASIMessage = MutableMapping[str, Any]


class WebSocketConnection:

    # TODO
    # - Implement ping/pong

    def __init__(
            self,
            send: Callable[[ASIMessage], Awaitable[None]],
            receive: Callable[[], Awaitable[ASIMessage]],
            subprotocols: Optional[List[str]] = None,
    ) -> None:
        self._send = send
        self._receive = receive
        self._subprotocols = subprotocols or []

    async def send(self, data: Union[str, bytes], *args, **kwargs) -> None:
        message: Dict[str, Union[str, bytes]] = {"type": "websocket.send"}

        if isinstance(data, bytes):
            message.update({"bytes": data})
        else:
            message.update({"text": str(data)})

        await self._send(message)

    async def recv(self, *args, **kwargs) -> Optional[str]:
        message = await self._receive()

        if message["type"] == "websocket.receive":
            return message["text"]
        elif message["type"] == "websocket.disconnect":
            pass

        return None

    receive = recv

    async def accept(self, subprotocols: Optional[List[str]] = None) -> None:
        subprotocol = None
        if subprotocols:
            for subp in subprotocols:
                if subp in self.subprotocols:
                    subprotocol = subp
                    break

        await self._send(
            {
                "type": "websocket.accept",
                "subprotocol": subprotocol,
            }
        )

    async def close(self) -> None:
        pass

    @property
    def subprotocols(self):
        return self._subprotocols

    @subprotocols.setter
    def subprotocols(self, subprotocols: Optional[List[str]] = None):
        self._subprotocols = subprotocols or []


class MockTransport:

    def __init__(
            self, scope, receive, send
    ) -> None:
        self.scope = scope
        self._receive = receive
        self._send = send
        self._protocol = None
        self.loop = None

    def get_websocket_connection(self) -> WebSocketConnection:
        try:
            return self._websocket_connection
        except AttributeError:
            raise ("Improper websocket connection.")

    def create_websocket_connection(
            self, send, receive
    ) -> WebSocketConnection:
        self._websocket_connection = WebSocketConnection(
            send, receive, self.scope.get("subprotocols", [])
        )
        return self._websocket_connection

    async def send(self, data) -> None:
        # TODO:
        # - Validation on data and that it is formatted properly and is valid
        await self._send(data)

    async def receive(self):
        return await self._receive()


class WsApp:

    def __init__(self, scope, receive, send) -> None:
        # self.scope = scope
        # self.receive = receive
        # self.send = send
        # self.ws = None
        self.transport = MockTransport(scope, receive, send)  # 这里对transport进行初始化,里面又用到了WebSocketConnection
        self.transport = self.transport.create_websocket_connection(send, receive)
        # self.asgi = False

    async def accept(self):
        await self.transport.accept()

    async def send(self, data):
        await self.transport.send(data)

    async def recv(self):
        return await self.transport.recv()

    def aaa(
            self,
            websocket_timeout=10,
            websocket_max_size=None,
            websocket_max_queue=None,
            websocket_read_limit=2 ** 16,
            websocket_write_limit=2 ** 16,
            websocket_ping_interval=20,
            websocket_ping_timeout=20,
            **kwargs,
    ):
        self.websocket = None
        # self.app = None
        self.websocket_timeout = websocket_timeout
        self.websocket_max_size = websocket_max_size
        self.websocket_max_queue = websocket_max_queue
        self.websocket_read_limit = websocket_read_limit
        self.websocket_write_limit = websocket_write_limit
        self.websocket_ping_interval = websocket_ping_interval
        self.websocket_ping_timeout = websocket_ping_timeout

    @classmethod
    async def __call__(self, scope, receive, send):
        # self.__init2__()
        # hook up the websocket protocol
        # if scope["type"] == "http":
        #     version = scope["http_version"]
        #     method = scope["method"]
        # elif scope["type"] == "websocket":
        #     version = "1.1"
        #     method = "GET"
        #
        # else:
        #     raise ("Received unknown ASGI scope")
        self.websocket = WebSocketCommonProtocol()
        # we use WebSocketCommonProtocol because we don't want the handshake
        # logic from WebSocketServerProtocol; however, we must tell it that
        # we're running on the server side
        self.websocket.is_client = False
        self.websocket.side = "server"
        # self.websocket.subprotocol = subprotocol
        self.websocket.connection_made(self.transport)
        self.websocket.connection_open()

        return self

    async def _websocket_handler(
            self, handler, request, *args, subprotocols=None, **kwargs
    ):
        request.app = self
        if self.asgi:
            # if True:
            ws = request.transport.get_websocket_connection()
            await ws.accept(subprotocols)
        else:
            protocol = request.transport.get_protocol()
            protocol.app = self

            ws = await protocol.websocket_handshake(request, subprotocols)

        # schedule the application handler
        # its future is kept in self.websocket_tasks in case it
        # needs to be cancelled due to the server being stopped
        handler(request, ws, *args, **kwargs)
        # fut = ensure_future(handler(request, ws, *args, **kwargs))
        # self.websocket_tasks.add(fut)
        try:
            await handler(request, ws, *args, **kwargs)
        except (ConnectionClosed):
            pass
        finally:
            # self.websocket_tasks.remove(fut)
            await ws.close()
