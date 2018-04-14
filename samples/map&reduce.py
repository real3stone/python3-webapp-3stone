# 【map/reduce】练习

# map(func， iterable):
# 把<函数func>作用到<序列iterable>中的每一个元素上

# reduce(func, iterable):
# 不同于map(), reduce()把每次func()的返回结果和序列iterable的下一个元素做累加运算


from functools import reduce


def fn(x, y):
    return x * 10 + y


print(reduce(fn, [1, 3, 5, 7, 9]))
# > 13579

# 廖大 本节后面布置的练习都没有做啊
