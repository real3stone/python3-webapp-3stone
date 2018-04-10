# 【协程coroutine】又称微线程，纤程
# 协程看上去也是子程序，但执行过程中，在子程序内部可中断，
# 然后转而执行别的子程序，在适当的时候再返回来接着执行
# 注意：在一个子程序中中断，去执行其他子程序，不是函数调用，有点类似CPU的中断

# **协程的特点在于是<一个线程>执行，那和多线程比，协程有何优势？
# 1、最大的优势就是协程极高的执行效率：因为子程序切换不是线程切换，而是由<程序自身>控制，
#   因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显
# 2、不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，
#   在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多

# **因为协程是一个线程执行，那怎么利用多核CPU呢？
# 最简单的方法是多进程+协程，既充分利用多核，又充分发挥协程的高效率，可获得极高的性能

# Python对协程的支持是通过generator(生成器)实现的


# yield 和 send 都可以理解为挂起(暂停)
# 分为两步执行：(以yield为例)
# 1、yield 先传值到send()挂起的地方，yield挂起，
# 2、等send()执行一次循环后返回，yield再执行其后的代码
# 3、知道又到yield，回步骤1


# 此函数时一个generator
def consumer():
    r = ''
    while True:
        # 1、给调用者返回r到send(),挂起 2、等send()执行一个循环后,接受其发回的值，赋给n
        n = yield r
        if not n:   # 调用者的send()函数没有发送回值
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'


def produce(c):
    c.send(None)  # 启动生成器(参数必须是None，否则启动需要用next()函数)
    n = 0
    while n < 5:
        n += 1  # 生产东西
        print('[PRODUCE Producing %s...' % n)
        # 1、给consumer()中yield挂起的地方返回r,挂起 2、等yield()执行一个循环后,接受其发回的值，赋给r
        r = c.send(n)
        print('[PRODUCE] Consumer return: %s' % r)
    c.close()  # produce决定不生产了，通过close()关闭consumer()

c = consumer()  # c是消费者对象，传入produce()
produce(c)

# 整个流程无锁，由一个线程执行，由consumer() 和 produce()协同完成，故称为协程

# 此时还没有实现多线程吧，不就是在两个函数里交替顺序执行吗？？？


