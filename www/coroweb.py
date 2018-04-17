#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '3stone'

import asyncio, os, inspect, logging, functools

from urllib import parse
from aiohttp import web
from apis import APIError


# 把一个函数映射为一个URL处理函数，即一个函数
# 通过@get修饰就附带了url信息
def get(path):
    '''
    Define decorator @get('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = 'path'
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
        wrapper.__route__ = 'path'
        return wrapper
    return decorator


# RequestHandler()目的是从URL函数中分析其需要接收得参数
# 从request中获取必要的参数，调用URL函数，然后把结果转换为web.request对象，
# 这样就完全符合aiohttp框架的要求了
class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn

    async def __call__(self, request):
        kw = 'waiting...'  # 获取参数
        r = await self._func(**kw)
        return r


# 用来注册一个URL处理函数
def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.route.add_route(method, path, RequestHandler(app, fn))





