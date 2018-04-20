# 【web框架】

# 由于我们的Web app建立在asyncio的基础上，因此用aiohttp写一个基本的app.py


import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime


from aiohttp import web
from jinja2 import Environment, FileSystemLoader

import orm
from coroweb import add_routes, add_static


# --------------------------- jinja2 ---------------------------
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    pass
    # ........

# ----------------------------- middleware --------------------------------------

# 【middleware】： 一种拦截器，一个URL在被某个函数处理前，可以经过一系列middleware处理
# 一个middleware可以改变URL的输入输出，甚至可以决定不继续处理而直接返回
# 因此middleware的【作用】：把通用的功能从各个URL处理函数中拿出来，几种放在一个地方。


# 记录URL的日志(middleware)
async def logger_factory(app, handler):
    async def logger(request):
        # 记录日志：
        logging.info('Request: %s %s' % (request.method, request.path))
        # 继续处理请求：
        return await handler(request)
    return logger


async def data_factory(app, handler):
    pass


# 把返回值转换为web.Response对象再返回 (middleware)
async def response_factory(app, handler):
    async def response(request):
        # 结果
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        # ......其他类型...

# 有了这些基础设施，我们就可以专注地往handler模块中添加URL处理函数了,可以极大提高效率


def datatime_filter(t):
    pass


async def init(loop):
    await orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='root', password='123456', database='awesome')
    # 注册对middleware和jinja2的支持
    app = web.Application(loop=loop, middlewares=[
                            logger_factory, response_factory
                          ])
    init_jinja2(app, filters=dict(datatime=datatime_filter))
    add_routes(app, 'handlers')  # 把handles模块中URL都加入进来
    add_static(app)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()




