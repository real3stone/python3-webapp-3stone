# 【web框架】

# 由于我们的Web app建立在asyncio的基础上，因此用aiohttp写一个基本的app.py


import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web


def index(request):
    # 不加headers参数，会以二进制文件的形式下载文件，而非生成网页（之后看看headers具体文档）
    return web.Response(body=b'<h1>Awesome</h1>', headers={'content-type': 'text/html'})


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()






