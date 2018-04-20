# 【异步IO - asyncio库】练习

# asyncio 是Python3.4版本引入的标注库，知己内置了对异步的IO支持；

# 异步操作需要在coroutine中通过yield from完成；
# 多个coroutine可以封装成 一组Task 然后并发执行


# 用asyncio的异步网络连接获取sina，souhu和163的网站首页(3个IO操作)
import asyncio


@asyncio.coroutine   # 定义好的装饰器，动态加入的功能是：把他放入消息队列EventLoop
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)  # 复习网络编程的内容
    reader, writer = yield from connect   # 读取时，可以跳去执行其他线程
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    # 逐行打印
    while True:
        line = yield from reader.readline()   # 读取时，可以跳去执行其他线程
        if line == b'\r\n':    # 读取完
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    # Ignore the body, close the socket
    writer.close()


loop = asyncio.get_event_loop()
# 三个连接由一个线程通过coroutine并发完成
tasks = [wget(host) for host in ['www.sina.com.cn', 'www.souhu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
