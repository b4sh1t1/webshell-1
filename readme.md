# webshell

一个前端操作虚拟机的demo,代码的主要逻辑基本可以直接使用,用了一些新特性他,基本每个依赖和库都是最新的. 也是一次对python异步和asgi的尝试.

## 技术栈

xterm + react + django3.2 + uvicorn + websocket + asyncio

## 后端

django3之后支持asgi,可以直接实现websoket,不用依赖channals库.
```shell 
pip3.8 install -r requirements.txt 
uvicorn app.asgi:application --reload
# 也可以自定义ping/pong间隔
uvicorn --log-level debug app.asgi:application --ws-ping-interval 10 --ws-ping-timeout 1
```
其中对ws协议的实现部分webshell/connection.py来自同样实现asgi的异步web框架fastapi(本质是来自starlette),如过不放心或着不知道如何使用可以参考这里
[starlette](https://www.starlette.io/websockets/)
处于好奇也看了sanic的ws实现,发现主要是使用了websockets这个库(uvicorn也是用的它)其中对ws协议的实现非常完整,我们这里的webshell/connection.py少了
ping/pong和max-size等特性的实现,但是对于当前的webhsell场景来说并不是必须的,如有需要uvicorn==0.15.0版本正好有参数可以控制.
## 前端
xterm的简单使用.
```shell
cd templates\web
npm install
npm start
```

调试ws的常用命令
```shell
> ws = new WebSocket('ws://localhost:8000/')
  WebSocket {url: "ws://localhost:8000/", readyState: 0, bufferedAmount: 0, onopen: null, onerror: null, …}
> ws.onmessage = event => console.log(event.data)
  event => console.log(event.data)
> ws.send("ping")
  undefined
  pong!

```