# 【aiohttp】HTTP异步框架

# 由于HTTP连接就是IO操作，因此可以用单线程+coroutine实现多用户的高并发支持

# asyncio实现了TCP、UDP、SSL等协议, aiohttp则是基于asyncio实现的HTTP框架!!!


# 实例：
# 分别处理两个URL
# / - 首页返回b'<h1>Index</h1>'
# /hello/{name} - 根据URL参数返回文本hello, %s!
import asyncio
from aiohttp import web


async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>', content_type='text/html')


async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'), content_type='text/html')


async def init(loop):  # aiohttp的初始化函数init()也是一个coroutine
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    # loop.create_server()则利用asyncio创建TCP服务
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

'''
其实aiohttp已经是一个web框架，但对于使用者来说，aiohttp相对比较底层
所以后边我们还需要自己封装一个框架

总结来说，aiohttp框架编写一个URL的处理函数，需要以下几步：
1、编写一个用@asyncio.coroutine装饰的函数
2、传入的参数需要自己从request中获取
3、需要自己构造response对象
而其实这些重复的工作可以由框架完成，具体看www/coroweb.py

'''



