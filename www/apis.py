#!/usr/bin/env python3
# -*- coding:utf-8 -*-


'''
JSON API definition

HTML页面中既包含数据又包含页面展示代码，虽然对用户来说阅读没问题，
但是对机器来说，从HTML中解析出数据很难

！如果一个URL返回的不是HTML，而是机器可以直接解析的数据，这个URL就可以看成是一个web API

由于API就是把web app的功能全部封装了，所以通过API操作数据，可以极大地把前端和后端的代码隔离

最常用的数据格式是JSON，JSON能直接被javascript读取
'''

import json, logging, inspect, functools


class APIError(Exception):
    '''
    the base APIError which contains error(requied), data(optional) and message(optional).
    '''
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message


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













