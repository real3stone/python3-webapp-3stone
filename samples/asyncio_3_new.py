# 【asyncio：简化代码的新语法】

# 旧语法：
# 用asyncio提供的@asyncio.coroutine可以把一个generator标记为coroutine类型
# 然后在coroutine内部用yield from调用另一个coroutine实现异步操作

# 新语法：
# 1、把asyncio.coroutine替换为 async
# 2、把yield from替换为 await

import asyncio

# 除了更换那两处，其他和asyncio_2.py相比都不变！
async def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)  # 复习网络编程的内容
    reader, writer = await connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    await writer.drain()
    while True:
        line = await reader.readline()
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

