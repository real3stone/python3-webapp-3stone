#!/usr/bin/env python3
# -*- coding:utf-8 -*-


'''
JSON API definition
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
    pass


class APIResourceNotFoundError(APIError):
    '''
    Indicate the resource was not found. The data specifies the resource name.
    '''
    pass


class APIPermissionError(APIError):
    '''
    Indicate the api has no permission.
    '''
    pass












