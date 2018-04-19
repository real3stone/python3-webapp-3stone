# 【面向对象高级编程】

# --------------------------- 定制类 ----------------------------


# __str__: 打印实例
class Student(object):

    def __init__(self, name):
        self.name = name

    # 用于打印Student对象实例
    def __str__(self):
        return 'Student object (name: %s)' % self.name

    def __call__(self):
        print('my name is %s' % self.name)

# __iter__: 返回一个迭代对象，然后，Python的for循环就会不断
#           调用该迭代对象的__next__()方法拿到循环的下一个值，
#           直到遇到StopIteration错误时退出循环

# 但是不能按下标取值(eg: Fib[3]), 但__getitem__可以像list一样访问class的实例

# __getitem__ （还有几个方法，可以使自定义类表现得像list，tuple，dict一样）


# 计算斐波那契数列
class Fib(object):
    def init(self):
        self.a, self.b = 0, 1  # 初始化两个计数器

    def __iter__(self):
        return self  # 实例本身就是迭代对象，故返回自己

    def __next__(self):

        self.a, self.b = self.b, self.a + self.b  # 计算下一个值
        if self.a > 1000:  # 退出循环
            raise StopIteration()
        return self.a  # 返回下一个值

    def __getitem__(self, n):  # 得到前n个斐波那契数
        a, b = 0, 1
        for x in range(n):
            a, b = b, a + b
        return a
        # 还可以在此定义类似于list的切片处理


# __getattr__: 动态返回属性（当找不到已定义属性时，会用__getattr__方法查找）

# ******* 链式动态匹配属性，没看懂，先跳过了！**********

# __call__: 使得实例本身可以直接类似于函数一样调用

#           用eg:callable(Student()) 判断一个对象是否能被调用

print(Student('3stone'))
s = Student('3stone')
s()
# 输出 my name is 3stone

for n in Fib():
    print(n)


# 【Python还有很多定制方法，本文只介绍了常用的几个】

# ------------------------- 枚举类 ------------------------------------
# 定义不可变的常量

from enum import Enum

# month类型的枚举类
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)




