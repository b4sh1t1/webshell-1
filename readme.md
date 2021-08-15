# webshell

## xterm + react + django3.2 + websocket + asyncio

## 后端

django3之后支持asgi,可以直接实现websoket,不用依赖channal库

pip3.8 install -r requirements.txt
uvicorn app.asgi:application --reload

## 前端
cd templates\web
npm install
npm start
