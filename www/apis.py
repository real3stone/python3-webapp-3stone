#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
JSON API definition
'''


# HTML页面中既包含数据又包含页面展示代码，虽然对用户来说阅读没问题，
# 但是对机器来说，从HTML中解析出数据很难

# 【web API】:如果一个URL(链接?)返回的不是HTML，而是机器可以直接解析的数据，这个URL就可以看成是一个web API

# REST(Representational State Transfer)风格：
# 一种设计API的模式，最常用的数据格式是JSON，JSON能直接被javascript读取，
# 因此以JSON格式编写的API简单，易读，易用

# 由于API就是把web app的功能全部封装了，所以通过API操作数据，可以极大地把前端和后端的代码隔离
# 一个API也是一个URL处理函数，我们希望通过<一个@api>把一个函数编程一个JSON格式的REST API

import json, logging, inspect, functools


# 【对Error进行处理】:这种Error是指调用API时发生的逻辑错误(eg:用户不存在)，其他错误视为bug，返回internalError

# 客户端调用API时，必须通过错误代码来区分API调用是否成功。错误代码是用来告诉调用者出错的原因。
# 很多API用一个整数表示错误码，这种方式很难维护错误码，客户端拿到错误码还需要查表得知错误信息。
# <更好的方式>是用字符串表示错误代码，不需要看文档也能猜到错误原因
class APIError(Exception):
    '''
    the base APIError which contains error(requied), data(optional) and message(optional).
    '''
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message


# 错误类型是为attributeError
class APIValueError(APIError):
    '''
    Indicate the input value has error or invalid.
    The data specifies the error field of input form
    '''
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:notfound', field, message)


class APIResourceNotFoundError(APIError):
    '''
    Indicate the resource was not found. The data specifies the resource name.
    '''
    def __init__(self, field, message=''):
        super(APIResourceNotFoundError, self).__init__('value:notfound', field, message)


class APIPermissionError(APIError):
    '''
    Indicate the api has no permission.
    '''
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)













