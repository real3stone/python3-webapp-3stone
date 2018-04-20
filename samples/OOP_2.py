# 【高级面向对象编程】-->【@property ; 多继承】

# 使用__slots__限制class实例能添加的属性
# __slots__仅对当前类实例起作用，对于继承的子类不起作用


# ------------------------ @property : 给类的方法加入生成器----------------------

# 既能检查参数，又可以用类似 属性 这样简单的方式来访问 类的变量

# decorator既可以给函数动态加上功能，对于<类的方法>，装饰器同样起作用,
# python内置的@property装饰器就是负责把一个<方法>变成<属性>调用的

# @property广泛应用在类的定义中，可以让调用者写出简短的代码，
# 同时保证对参数进行必要的检查，这样，程序运行时就减少了出错的可能性。


class Student(object):
    # __slots__ = ('name', 'age')  # 用tuple定义允许绑定的属性名称，即只能赋值name,age

    @property
    def score(self):
        return self._score

    @score.setter  # property本身又创造了一个装饰器
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an interget!')
        if value < 0 or value > 100:
            raise ValueError('score must be between 0`100!')
        self._score = value


class Screen(object):

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        # 此处可加入参数检查嘛！
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property               # resolution是只读属性
    def resolution(self):
        return self._height * self._width

s = Screen()
s.width = 3
s.height = 4
print(s.resolution)

# @property广泛应用在类的定义中，可以让调用者写出简短的代码，
# 同时保证对参数进行必要的检查，这样，程序运行时就减少了出错的可能性。

# -------------------------------------------------------------------------

# ----------------------------多继承----------------------------------------

# 通过多继承，一个子类可以同时获得多个父类的所有功能（区别于Java-单继承）

# 命名时用后缀MixIn区分继承的主线和分支
# MixIn的目的是给一个了增加多个功能，
# 即在设计类时优先考虑通过多重继承来组合多个MixIn功能，而不是设计多层次的复杂的继承关系
# 我们不需要复杂而庞大的继承链，只要选择组合不同的类的功能，就可以快速构造出所需的子类
# -------------------------------------------------------------------------





