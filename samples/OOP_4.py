# 【面向对象高级编程】-元类

# 动态语言和静态语言最大的不同，就是类和函数的定义，不是编译时定义的，而是运行时动态创建的

# type()函数：
# 1、可以查看一个类型或变量的类型
# 2、可以创建出新的类（Python支持用type()在运行期动态创建类）


# metaclass(元类)：控制类的创建行为(如：增加一些属性，方法等)--动态修改！！

# <简单解释>：我们定义了类之后可以根据这个元类(metaclass)创建出实例，
# 故：先定义类，后创建实例；而要创建类，需先定义metaclass
# 你可以把 类 看成是metaclass创造出来的实例


# metaclass是类的模板，所以必须从'type'类型派生
class ListMetaclass(type):
    # 给我们自定义的MyList类增加一个add方法
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)

# __new__()方法接收到的参数依次是：
# 1、当前准备创建的类的对象；
# 2、类的名字；
# 3、类继承的父类集合
# 4、类的方法集合


# 定义类时，传入metaclass参数，指示使用ListMetaclass来定制类
# 这样Python解释器在创建MyList时，就会通过ListMetaclass.__new__()来创建
class MyList(list, metaclass=ListMetaclass):
    pass


# 动态修改的意义：
# 需要通过metaclass修改类定义的情况之一：ORM（Object Rational Mapping））
# 即 对象-关系映射：把<关系数据库的一行>映射为<一个对象>，也就是<一个类>代表<一个表>

# 要编写一个ORM框架，所有的类都只能动态定义，因为只有使用者才能根据标的表的结构定义出对应的类来

'''
ORM框架：分为三个 .py 文件
            orm.py
            model.py
            use_orm.py
'''




