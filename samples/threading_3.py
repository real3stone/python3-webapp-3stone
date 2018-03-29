# 【ThreadLocal】局部变量

# 全局变量需要加锁，使用局部变量更佳！
# 但局部变量在函数调用时传递很麻烦, 使用ThreadLocal简化过程

# ******************************************************************
# 一个ThreadLocal变量虽然是全局变量，
# 但每个线程都只能读写自己线程的独立副本，互不干扰
# 【可以理解为一个已经封装好的dict，自动匹配当前进程】【是不是有点多态的意思】
# ThreadLocal解决了参数在一个线程中各个函数之间互相传递的问题

# ThreadLocal最常用的地方就是为每个线程绑定一个数据库连接，HTTP请求，用户身份信息等，
# 这样一个线程的所有调用到的处理函数都可以非常方便地访问这些资源。
# *******************************************************************
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading


local_school = threading.local()


def process_student():
    # 获取当前线程关联的student
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))
    age = local_school.age
    print('sum: %s' % age)


def process_thread(name, age):
    # 绑定ThreadLocal的student:
    local_school.student = name
    local_school.age = age
    process_student()


t1 = threading.Thread(target=process_thread, args=('Alice', '20',), name='Thread-1')
t2 = threading.Thread(target=process_thread, args=('3stone', '24',), name='Thread-2')
t1.start()
t2.start()
t1.join()
t2.join()






