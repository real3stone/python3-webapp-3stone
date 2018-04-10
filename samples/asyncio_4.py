# 【aiohttp】服务器端使用asyncio


# 由于HTTP连接就是IO操作，因此可以用单线程+coroutine实现多用户的高并发支持

# asyncio实现了TCP、UDP、SSL等协议,aiohttp则是基于asyncio实现的HTTP框架


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


async def init(loop):  # 也是一个协程
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv


loop = asyncio.get_event_loop()
loop.run_untilx_complete(init(loop))
loop.run_forever()





