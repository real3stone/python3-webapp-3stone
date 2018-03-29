# 【线程锁--lock】

import threading

# 多线程和多进程最大的不同在于，
# 多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，
# 而多线程中，所有变量都由所有线程共享，
# 所以，任何一个变量都可以被任何一个线程修改，
# 因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了。


# ****************** 实例：多线程同时操作一个变量 **************************************


# 假定这是你的银行账户
balance = 0
lock = threading.Lock()  # 锁


def change_it(n):
    # 先存后取，结果应该为0：
    global balance
    balance += n   # 加减操作之间有可能被中断，进而导致修改不一致
    balance -= n


# 不加锁
def run_thread(n):
    for i in range(100000):
        change_it(n)


# 给函数change_it()加锁
def run_thread_with_lock(n):
    for i in range(100000):
        # 先要获取锁
        lock.acquire()
        try:
            # 放心地改balance吧
            change_it(n)
        finally:
            # 改完了一定要释放锁
            lock.release()


# 启动两个线程
# t1 = threading.Thread(target=run_thread, args=(5,))
# t2 = threading.Thread(target=run_thread, args=(8,))
t1 = threading.Thread(target=run_thread_with_lock, args=(5,))
t2 = threading.Thread(target=run_thread_with_lock, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print('final result: balance = %s' % balance)
# 由于线程的调度是由操作系统决定的，当t1、t2交替执行时，
# 只要循环次数足够多，balance的结果就不一定是0了

# ************************** lock 锁 *****************************
# 锁的好处就是确保了某段关键代码只能由一个线程从头到尾完整地执行，
# 坏处当然也很多，首先是阻止了多线程并发执行，
# 包含锁的某段代码实际上只能以单线程模式执行，效率就大大地下降了。
# 其次，由于可以存在多个锁，不同的线程持有不同的锁，并试图获取对方持有的锁时，
# 可能会造成死锁，导致多个线程全部挂起，既不能执行，也无法结束，只能靠操作系统强制终止。

# ************************ 多核任务 ********************
# Python解释器由于涉及是有GIL全局锁，导致了多线程无法利用多核。
# 多线程的并发在Python中那一实现
# 可以用多进程实现多核任务



