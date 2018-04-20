#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'url handerls'

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from models import User, Comment, Blog, next_id


@get('/')
def index(request):
    # 不加content_type参数，会以二进制文件的形式下载文件，而非生成网页（之后看看具体文档）
    users = yield from User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }
    # return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')


