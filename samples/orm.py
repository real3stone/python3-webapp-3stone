# 【ORM框架】练习


# Field类，复习保存数据库表的 字段名 和 字段类型
class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class StringField(Field):

    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')


class IntegerField(Field):

    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')


class ModelMetaclass(type):
    '''
    metaclass 做了3件事：
    1、排除掉对Model类的修改
    2、在当前类中（比如 User）中查找定义的类的所有属性，如果找到一个Field属性，
        就把他保存到一个__mappings__的dict中，同时从类属性中删除该Field属性
    3、把表名保存到__table__中，如果还有其他属性同样如此保存
    '''

    def __new__(cls, name, bases, attrs):

        if name == 'Model':   # 排除掉对Model类的修改
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)

        mappings = dict()
        for k, v in attrs.items():  # 在当前类(User)中查找定义的类的所有属性
            if isinstance(v, Field):   # 如果找到一个Field属性，就把他保存到一个__mappings__的dict中
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():  # 找到的同时，从类属性中删除该Field属性
            attrs.pop(k)
        attrs['__mappings__'] = mappings  # 保存刚查找到的 属性和列的关系
        attrs['__table__'] = name  # 把表名保存到__table__中(假设表名和类名一致)
        # type可以实现运行期动态创建类
        return type.__new__(cls, name, bases, attrs)  # ？？？


# 基类 Model
# 可以定义各种操作数据库的方法
class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):  # 保存一个实例到数据库
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)  # 保存在mappings中的属性值
            params.append('?')  # 参数值(就是'?'组成的list)
            args.append(getattr(self, k, None))    # 取出Model的属性值
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        # 此处因为没有连接数据库，所以没有执行sql语句，只是打印出来了
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))




