# 【装饰器decorator】

# 在代码运行期动态增加函数的功能!!!

# 本质上就是返回函数的高阶函数
# 用@调用装饰器，传入函数对象


import functools
import time


# 加入装饰器后，原来的now函数仍然存在，只是函数名now已经指向了log内的wrapper()
# 而wrapper()是在now()的基础上加入了 <打印日志> 的功能


# 如果decorator本身需要传入参数，则需要编写一个返回decorator的高阶函数
# eg: 自定义log的文本
def log(text=None):
    def decorator(func):
        @functools.wraps(func)  # 先记住，没讲原理(标记decorator？)
        def wrapper(*args, **kw):
            if callable(text):
                print('call %s()' % func.__name__)
            else:
                print('%s %s()' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


@log()
def now_1():
    print('test_1!')


@log('execute')   # 相当于执行：now = log('execute')(now)
def now_2():
    print('test_2')
# 分析：先执行log('execute'),返回的是decorator函数，再调用，返回值是wrapper()

now_2()


# 如何实现log() 和 log('execute')同时使用？


# 打印一个函数运行的时间
def total_runtime(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        start_moment = time.time()
        result_of_func = func(*args, **kw)
        end_moment = time.time()
        # 字符串怎样转化为int相减
        print('Total_time_of_%s: %s' % (func.__name__, (float(end_moment) - float(start_moment))))
        return result_of_func
    return wrapper


@total_runtime
def fast(x, y):
    time.sleep(0.0012)
    return x + y

f = fast(11, 22)


