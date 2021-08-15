https://hub.fastgit.org/j-yeskay/chatscape-django/blob/main/chat/consumers.py

https://hub.fastgit.org/jimmy201602/webterminal

https://hub.fastgit.org/wanglu58/webssh/blob/master/static/webssh.js
https://hub.fastgit.org/wanglu58/webssh

WebSSH动态调整终端窗口大小
如果我中途调整了浏览器的大小，显示就乱了，这该怎么办？ 好办， 终端窗口的大小需要浏览器和后端返回的Terminal大小保持一致，单单调整页面窗口大小或者后端返回的Terminal窗口大小都是不行的，那么从这两个方向来说明该如何动态调整窗口的大小 。

首先Paramiko模块建立的SSH通道可以通过resize_pty来动态改变返回Terminal窗口的大小，使用方法如下：

def resize_pty(self, cols, rows):
    self.ssh_channel.resize_pty(width=cols, height=rows)
然后Django的Channels每次接收到前端发过来的数据时，判断一下窗口是否有变化，如果有变化则调用上边的方法动态改变Terminal输出窗口的大小

我在实现时会给传过来的数据加个status，如果status不是0，则调用resize_pty的方法动态调整窗口大小，否则就正常调用执行命令的方法，代码如下：

def receive(self, text_data=None, bytes_data=None):
    if text_data is None:
        self.ssh.django_bytes_to_ssh(bytes_data)
    else:
        data = json.loads(text_data)
        if type(data) == dict:
            status = data['status']
            if status == 0:
                data = data['data']

                self.ssh.shell(data)
            else:
                cols = data['cols']
                rows = data['rows']
                self.ssh.resize_pty(cols=cols, rows=rows)


https://hub.fastgit.org/YashGupta534/django-websocket/tree/master/websocket

https://jaydenwindle.com/writing/django-websockets-zero-dependenci


https://hub.fastgit.org/YashGupta534/django-websocket/tree/master/websocket
https://aliashkevich.com/websockets-in-django-3-1/


https://websockets.readthedocs.io/en/stable/faq.html#server-side

How do I run a HTTP server and WebSocket server on the same port?

    This isn’t supported.
    
    Providing a HTTP server is out of scope for websockets. It only aims at providing a WebSocket server.
    
    There’s limited support for returning HTTP responses with the process_request hook. If you need more, pick a HTTP server and run it separately.
    

WebSockets状态码

WebSockets 的CloseEvent 会在连接关闭时发送给使用 WebSockets 的客户端。它在 WebSocket 对象的 onclose 事件监听器中使用。服务端发送的关闭码，以下为已分配的状态码。

状态码 名称 描述

    0–999 - 保留段, 未使用。
    1000 CLOSE_NORMAL 正常关闭; 无论为何目的而创建, 该链接都已成功完成任务。
    1001 CLOSE_GOING_AWAY 终端离开, 可能因为服务端错误, 也可能因为浏览器正从打开连接的页面跳转离开。
    1002 CLOSE_PROTOCOL_ERROR 由于协议错误而中断连接。
    1003 CLOSE_UNSUPPORTED 由于接收到不允许的数据类型而断开连接 (如仅接收文本数据的终端接收到了二进制数据)。
    1004 - 保留。 其意义可能会在未来定义。
    1005 CLOSE_NO_STATUS 保留。 表示没有收到预期的状态码。
    1006 CLOSE_ABNORMAL 保留。 用于期望收到状态码时连接非正常关闭 (也就是说, 没有发送关闭帧)。
    1007 Unsupported Data 由于收到了格式不符的数据而断开连接 (如文本消息中包含了非 UTF-8 数据)。
    1008 Policy Violation 由于收到不符合约定的数据而断开连接。 这是一个通用状态码, 用于不适合使用 1003 和 1009 状态码的场景。
    1009 CLOSE_TOO_LARGE 由于收到过大的数据帧而断开连接。
    1010 Missing Extension 客户端期望服务器商定一个或多个拓展, 但服务器没有处理, 因此客户端断开连接。
    1011 Internal Error 客户端由于遇到没有预料的情况阻止其完成请求, 因此服务端断开连接。
    1012 Service Restart 服务器由于重启而断开连接。 [Ref]
    1013 Try Again Later 服务器由于临时原因断开连接, 如服务器过载因此断开一部分客户端连接。 [Ref]
    1014 - 由 WebSocket 标准保留以便未来使用。
    1015 TLS Handshake 保留。 表示连接由于无法完成 TLS 握手而关闭 (例如无法验证服务器证书)。
    1016–1999 - 由 WebSocket 标准保留以便未来使用。
    2000–2999 - 由 WebSocket 拓展保留使用。
    3000–3999 - 可以由库或框架使用。 不应由应用使用。 可以在 IANA 注册, 先到先得。
    4000–4999 - 可以由应用使用。


```shell
> ws = new WebSocket('ws://localhost:8000/')
  WebSocket {url: "ws://localhost:8000/", readyState: 0, bufferedAmount: 0, onopen: null, onerror: null, …}
> ws.onmessage = event => console.log(event.data)
  event => console.log(event.data)
> ws.send("ping")
  undefined
  pong!

```

F:\Python38\Lib\site-packages\websockets\legacy\protocol.py

