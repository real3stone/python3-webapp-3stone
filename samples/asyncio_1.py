# 【异步IO】练习

# asyncio是Python的标准库，编程模型为一个消息循环
# 从asyncio模块中直接获取一个EventLoop的应用，然后把需要执行的协程扔EventLoop
# 中执行，就实现了异步IO
import asyncio
import threading


# 用asyncio实现hello world代码
@asyncio.coroutine
def hello():
    print('Hello world!')
    # 异步调用asyncio.sleep(1):
    r = yield from asyncio.sleep(1)
    print('Hello  again!')

# 获取EventLoop：
loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
# 执行coroutine
loop.run_until_complete(asyncio.wait(tasks))
loop.close()



