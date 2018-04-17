# 【高级面向对象编程】笔记

# ------------------------ @property ----------------------------------
# 使用__slots__限制class实例能添加的属性
# __slots__仅对当前类实例起作用，对于继承的子类不起作用

# python内置的@property装饰器就是负责把一个方法编程属性调用的


class Student(object):
    # __slots__ = ('name', 'age')  # 用tuple定义允许绑定的属性名称，即只能赋值name，age

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

    @property
    def resolution(self):
        return self._height * self._width

# --------------------------------------------------------------

# ----------------------------多继承----------------------------------

# 通过多继承，一个子类可以同时获得多个父类的所有功能（区别于Java）

# 命名时用后缀MixIn区分继承的主线


