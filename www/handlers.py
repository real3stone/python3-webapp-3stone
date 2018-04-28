#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'url handerls'

import re, time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
from models import User, Comment, Blog, next_id
from apis import APIError, APIValueError, APIResourceNotFoundError


from aiohttp import web

from config import configs

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret


# 计算加密cookie
def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


# 计算解密cookie
async def cookie2user(cookie_str):
    '''
    Paras cookie and load user if cookie is valid
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():  # 超过有效时间
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('################invalid sha1###############')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None


# 利用web框架的@get和ORM框架的Model支持，编写一个处理首页URL的函数
@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'

    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
        '__template__': 'blogs.html',    # 模板文件是test.html
        'blogs': blogs                  # 传递给模板的参数
    }


# 这个URL的作用：把users的数据信息，以JSON格式封装在web.response()中返回（服务于计算机获取数据？）
@get('/api/users')
async def api_get_users(*, page='1'):
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'   # 返回时 隐藏密码
    return dict(users=users)
    # 只需返回一个dict，app.py中的response()这个middleware就可以把dict序列化成JSON格式


# 验证邮箱格式是否正确
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
# 验证SHA1编码是否正确
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


# 用户注册
@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }


# 用户注册api
@post('/api/users')
async def api_registers_user(*, email, name, passwd):
    # ---检查数据---
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = await User.findAll('email=?', [email])

    # 数据库已有该邮箱记录，即已注册
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    # --- 注册 ---
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()

    # make session cookie
    # 制作会话cookie，返回客户端浏览器
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


# 用户登录
@get('/signin')
async def singin():
    return {
        '__template__': 'signin.html'
    }


# 用户登录api
@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid Email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid passwd')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        # 这儿为什么不匹配呢？因为之前的密码都保存的是原始，行生成的是sha1处理过的？
        # 那就重新先把register.py调通再说.
        raise APIValueError('passwd', 'Wrong password!')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=86400)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r








