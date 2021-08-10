import asyncio


async def test1():
    while True:
        await asyncio.sleep(0.01)
        print("test1")


async def test2():
    while True:
        await asyncio.sleep(0.01)
        print("test2")


async def mian():
    # 这么写并不能打破while循环切换调度
    # await test1()
    # await test2()

    # 需要这么写才行
    await asyncio.gather(test1(), test2())


loop = asyncio.get_event_loop()
loop.run_until_complete(mian())
