#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'url handerls'

import re, time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
from models import User, Comment, Blog, next_id


@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }


@get('/3stone')
async def test_1(request):
    users = await User.findNum('name')
    return {
        '__template__': 'test.html',
        'users': users
    }


