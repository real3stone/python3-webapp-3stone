# 【进程 池】


# multiprocessing模块提供了一个Process类来代表一个进程对象
from multiprocessing import Process
# 需要启动大量的子进程，可以用进程池
from multiprocessing import Pool
import os
import time
import random


# 子进程要执行的代码
def run_process(name):
    print('Run child process %s ( %s)...' % (name, os.getpid()))

if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_process, args=('test',))  # 创建Process实例
    print('Child process will start.')
    p.start()
    p.join()  # join()方法可以等待子进程结束后再继续往下运行，通常用于进程的同步
    print('Child process end.')


# ************** 进程池  Pool *****************************


# 计算随机睡眠时间
def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)   # 设置进程池的默认大小，即同时可执行的进程数
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocess done...')
    p.close()  # 调用join()前必须先调用close(),调用close()后就不能继续添加新的Process了
    p.join()   # 对Pool对象调用join()方法会等待所有子进程执行完毕，
    print('All subprocess done.')






