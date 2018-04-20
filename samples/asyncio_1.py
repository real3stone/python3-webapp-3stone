# 【异步IO - Python库asyncio】用sleep()模拟IO操作

# asyncio是Python的标准库，编程模型为一个消息循环(EventLoop)
# 从asyncio模块中直接获取一个EventLoop的应用，
# 然后把需要执行的协程扔EventLoop中执行，就实现了异步IO
import asyncio
import threading


# 用asyncio实现hello world 并发
@asyncio.coroutine  # 把一个generator标记为coroutine类型(装饰器)，装饰器作用是把这个coroutine扔到EventLoop中
def hello(n):
    print('Hello world - %s! (%s)' % (n, threading.current_thread()))
    # 异步调用asyncio.sleep(1):
    # 由于asyncio.sleep()也是一个coroutine，
    # 所以线程不会等待asyncio.sleep()，而是直接中断并执行下一个消息循环
    r = yield from asyncio.sleep(1)
    # 当asyncio.sleep()返回时，
    # 线程就可以从yield from拿到返回值（此处是None），然后接着执行下一行语句
    print('Hello  again - %s! (%s)' % (n, threading.current_thread()))

# 把asyncio.sleep(1)看成是一个耗时1秒的IO操作，在此期间，主线程并未等待，
# 而是去执行 EventLoop中 其他可以执行的coroutine了，因此可以实现并发执行

# 获取EventLoop：
loop = asyncio.get_event_loop()
tasks = [hello(0), hello(1), hello(3)]
# 执行coroutine
loop.run_until_complete(asyncio.wait(tasks))
loop.close()


# 由打印的结果可见，3个coroutine是由同一个线程并发执行的
