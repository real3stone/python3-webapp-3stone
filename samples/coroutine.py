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


# 此函数时一个generator
def consumer():
    r = ''
    while True:
        n = yield r  # 通过yield拿到消息,处理完,又通过yield返回
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'


def produce(c):
    c.send(None)  # 启动生成器
    n = 0
    while n < 5:
        n += 1
        print('[PRODUCE Producing %s...' % n)
        r = c.send(n)  # 切换到consumer(),使其通过yield拿到消息,等返回后再赋值给r
        print('[PRODUCE] Consumer return: %s' % r)
    c.close()  # produce决定不生产了，通过close()关闭consumer()

c = consumer()
produce(c)

