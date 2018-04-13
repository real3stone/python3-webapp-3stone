'''
# 【封装数据库操作】


# 我们的web框架使用了基于asyncio的aiohttp，这是基于协程的异步模型
# 在协程中不能调用普通的同步IO操作，因为速度不匹配(详见廖雪峰教程day3)

# 这是异步编程的一个原则：一旦决定使用异步，则系统的每一步都必须是异步的

# aiomysql为MySQL数据库提供了异步IO的驱动
'''
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiomysql
import logging; logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time


# 廖大部分代码没有粘在教程里； 记录日志？？
def log(sql, args=()):
    logging.info('SQL: %s' % sql)


# 创建连接池
@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['123456'],
        db=kw['db'],
        charset=kw.get('charset', 'utf-8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )


# 封装select语句
@asyncio.coroutine
def select(sql, args, size=None):
    log(sql, args)
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs
# 注意要始终坚持使用带参数的SQL，而不是自己拼接SQL字符串，这样可以防止SQL注入攻击


# 封装insert, update, delete
# 要执行INSERT、UPDATE、DELETE语句，可以定义一个通用的execute()函数，
# 因为这3种SQL的执行都需要相同的参数，以及返回一个整数表示影响的行数
@asyncio.coroutine
def execute(sql, args):
    log(sql)
    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursor()
            yield from cur.execute(sql.replace('?', '%s'), args)
            affected = cur.worcount
            yield from cur.close()
        except BaseException as e:
            raise   # 上抛
        return affected
# execute()函数和select()函数所不同的是，cursor对象不返回结果集，而是通过rowcount返回结果数


# 什么函数？作用？
def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


# Field及其子类
class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


# 映射varchar的StringField
class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)  # 多重继承 初始化


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


# Model只是一个基类，如何将具体的子类如User的映射信息读取出来呢？通过metaclass：ModelMetaclass
class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):

        # 排除Model类本身
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        # 获取table名称：
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))

        # 获取所有的Field和主键名：
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info(' found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键
                    if primaryKey:
                        raise RuntimeError('Duplication primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key no found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s' % f, fields))
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        # 构造默认的select，insert，update和delete语句
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
            tableName,  ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1)
        )
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
            tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey
        )
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)
        # 这样继承自Model的类会自动通过ModelMetaclass扫描映射关系，并存储到自身类属性如__table__, __mappings__中


# 首先定义所有ORM映射的基类
# Model从dict继承，所以具备所有<dict的功能>，同时实现方法__getattr__()和__setattr__()
# 因此可以向应用普通字段那样写，eg:user['id'] 和user.id 均输出123
class Model(dict, metaclass=ModelMetaclass):

    # 【构造方法】:当实例被初始化时被调用。注意名字前后的双下划线，这是表明这个属
    # 性或方法对Python有特殊意义，但是允许用户自行定义。你自己取名时不应该用这种格式
    def __init__(self, **kw):  # ？？？？
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attibute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    # 【实例方法】:第一个参数总是self，就是这个实例对象
    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod   # 【类方法】:被所有此类的实例所共用，第一个参数cls就是这个<类 对象>
    async def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause. '
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def find(cls, pk):
        ' find object by primary key. '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)





