#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, os, inspect, logging, functools

from urllib import parse
from aiohttp import web
from apis import APIError


# 装饰器： 把一个函数映射为一个URL处理函数，这样一个函数通过@get修饰就附带了url信息
def get(path):
    '''
    Define decorator @get('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'  # 附加URL信息
        wrapper.__route__ = path
        return wrapper
    return decorator


def post(path):
    '''
    Define decorator @post('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator


# URL处理函数不一定是一个coroutine，我们用RequestHandler()封装一个URL处理函数


# RequestHandler()目的：从URL函数中分析其需要接收的参数；
# 从request中获取必要的参数，调用URL函数，然后把结果转换为web.request对象
# 这样就完全符合aiohttp框架的要求了
class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn
    # 虽然requestHandler()是一个类，但定义了__call__()方法，其实例就可被视为函数
    async def __call__(self, request):
        kw = None  #
        r = await self._func(**kw)
        return r


# ?????
def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))


# 用来注册一个URL处理函数
def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    # 判断是否为协程？？
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__,
                                                ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))


# 自动把 module_name模块 中所有符合条件的函数都注册了
def add_routes(app, module_name):
    n = module_name.rfind('.')  # rfind 返回字符串最后出现的位置，匹配失败返回-1
    if n == (-1):  # __import__：运行时动态加载模块，返回属性和方法列表 or 模块？关键要和else中的mod对应哪
        mod = __import__(module_name, globals(), locals())
    else:     # 嵌套结构，找到模块最后一部分(wg:www.orm,取出orm) 但下面的__import__没看懂啊
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):         # dir(): 获取mod的 属性和方法 列表
        if attr.startswith('_'):   # 对'_'开头的不操作
            continue
        fn = getattr(mod, attr)   # 获取attr代指的方法
        if callable(fn):          # 判断是否可调用（即 是否为函数）
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)  # 加入URL




