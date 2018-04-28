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


# 记录对数据库的操作日志
def log(sql, args=()):
    logging.info('SQL: %s' % sql)


# 创建连接池
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool   # 全局变量__pool存储连接池
    # 使用mysql异步驱动模块：aiomysql
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['database'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )


# 关闭连接池（根据讨论自加，不加会报错：Event Loop is closed）
async def destroy_pool():
    global __pool
    if __pool is not None:
        __pool.close()
        await __pool.wait_closed()


# 封装select语句
async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    async with __pool.get() as conn:  # with 打开（代替try...execept...简化代码）
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?', '%s'), args or ())  # sql语句的占位符是'?',mysql的占位符是'%s',替换
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs
# 注意要始终坚持使用带参数的SQL，而不是自己拼接SQL字符串，这样可以防止SQL注入攻击


# 封装insert, update, delete
# 要执行INSERT、UPDATE、DELETE语句，可以定义一个通用的execute()函数，
# 因为这3种SQL的执行都需要相同的参数，以及返回一个整数表示影响的行数
async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:   # 从线程池中获取一个线程，命名为conn(R:with语法->IO)
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)  # sql语句的占位符是'?',mysql的占位符是'%s',替换
                affected = cur.rowcount  # 行数
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected  # 返回行数
# execute()函数和select()函数所不同的是，cursor对象不返回结果集，而是通过rowcount返回结果数


# 构造sql语句需要的字符串: (?,?,?,?,?)
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
        # 给Field增加一个default参数可以让ORM自己填入缺省值，
        # 并且缺省值可以作为函数对象传入，如主键id的default是next_id()函数，在调用save()时自动计算

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


# Model只是一个基类，如何将具体的子类如User的映射信息读取出来呢？通过metaclass
class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):  # 初始化一个新的model实例

        # 排除Model类本身
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        # 获取table名称：
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))

        # 获取所有的Field和主键名：
        mappings = dict()
        fields = []  # 保存属性名的列表？
        primaryKey = None

        for k, v in attrs.items():
            if isinstance(v, Field):  # Field算是什么类别呢？映射字符、数字等数据的格式
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
        # 给fields中保存的每个属性名加上'``'后，变成列表格式（mysql中`id`是查询时列的格式，但自己尝试貌似不佳``也可以查询哪）
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        # 构造默认的select，insert，update和delete 的sql语句
        # 封装成Model类型的方法直接使用！
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
        tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
        tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)
        # 这样继承自Model的类(eg:Users)会自动通过ModelMetaclass扫描映射关系，
        # 并存储到自身类属性如__table__, __mappings__中


# 首先定义所有ORM映射的基类
# Model从dict继承，所以具备所有<dict的功能>，同时实现方法__getattr__()和__setattr__()
# 因此可以向应用普通字段那样写，eg:user['id'] 和user.id 均输出123
class Model(dict, metaclass=ModelMetaclass):

    # 【构造方法】:当实例被初始化时被调用。注意名字前后的双下划线，这是表明这个属
    # 性或方法对Python有特殊意义，但是允许用户自行定义。你自己取名时不应该用这种格式
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):   # 获取属性key的值
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attibute '%s'" % key)

    def __setattr__(self, key, value):   # 设置属性key的值
        self[key] = value

    # 【实例方法】:第一个参数总是self，就是这个实例对象
    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:  # key没有对应值
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default  # ？？
                # 记录日志：返回了默认值
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod   # 【类方法】:被所有此类的实例所共用，第一个参数cls就是这个<类 对象>
    async def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause. '

        # 根据where条件 和 可变参数kw 拼接出sql语句
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
        # 执行sql语句
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
        return rs[0]['_num_']  # 返回数量

    @classmethod
    async def find(cls, pk):
        ' find object by primary key. '
        # 拼接出select()函数需要的参数
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        # 把Model实例的属性组成list，作为参数传入execute()方法，即插入数据库

        # map()函数：把从fields中得到除主键外的每个属性名，传入geValueOrDefault()函数得到具体值
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))  # list中补充主键
        # 这里的__insert__,应该是metaclass映射过来的
        rows = await execute(self.__insert__, args)
        if rows != 1:                                    # 判断是否 插入成功
            logging.warn('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]  # 删除只用获取主键即可
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)




