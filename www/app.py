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
# 大佬貌似没讲怎么用jinja2模板啊！以后用都这样套模板？还是说自己去瞅jinja2文档？
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape=kw.get('autoescape', True),
        block_start_string=kw.get('block_start_string', '{%'),
        block_end_string=kw.get('block_end_string', '%}'),
        variable_start_string=kw.get('variable_start_string', '{{'),
        variable_end_string=kw.get('variable_end_sting', '}}'),
        auto_reload=kw.get('auto_reload', True)
    )
    path = kw.get('path', None)  # 设置jinja2 templates路径
    if path is None:    # 获取路径 D:\0code\python\python3-webapp-3stone\www\templates
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 templates path: %s' % path)

    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)

    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env   # 注册jinja2模板 www/templates 给app

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
        return await handler(request)  # 所以handler()到底是什么函数？
    return logger    # 返回函数 装饰器？？


# 把数据怎么着了????
async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()   # json格式
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www/form-urlencoded'):
                request.__data__ = await request.post()   # 另一种格式？
                logging.info('request form: %s' % str(request.__data__))
        return await handler(request)
    return parse_data


# 把返回值转换为web.Response对象再返回 (middleware)
async def response_factory(app, handler):
    async def response(request):
        # 结果
        r = await handler(request)
        if isinstance(r, web.StreamResponse):   # 流
            return r
        if isinstance(r, bytes):   # 二进制
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):     # 字符串
            if r.startswith('redirect:'):  # 重定位？
                return web.HTTPFound(r[9:])   # 除去'resirect:'这九个字符
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):   # 字典
            template = r.get('__template__')
            if template is None:  # json形式返回
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:                  # html形式返回
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int):     # 整形
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:  # tuple
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(t, str(m))

        # default 默认值
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response


# 有了这些基础设施，我们就可以专注地往handler模块中添加URL处理函数了,可以极大提高效率

# 时间过滤
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


async def init(loop):
    await orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='root', password='123456', database='awesome')
    # 注册对middleware和jinja2的支持
    app = web.Application(loop=loop, middlewares=[
                            logger_factory, response_factory
                          ])
    init_jinja2(app, filters=dict(datatime=datetime_filter))  # 初始化jinja2模板
    add_routes(app, 'handlers')  # 把handles模块中URL都加入进来
    add_static(app)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()




