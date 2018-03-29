# 【线程】 初步


# Python标准库提供两个模块：_thread & threading，
# _thread是低级模块，threading是高级模块并对_thread进行了封装
# 绝大多数情况下，只需要使用threading模块即可
import time
import threading


# 启动一个线程就是把一个函数传入并创建Thread实例，然后start()开始执行
def loop():  # 新线程执行的代码
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n += 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)  # 删去这一句就能看到两个线程每次输出的不同，即推进的不确定性
    print('thread %s ended.' % threading.current_thread().name)


def check():
    print('thread %s is running...' % threading.current_thread().name)
    new_list = ['a', 'b', 'c', 'd']
    for x in new_list:
        print('thread %s >>> %s' % (threading.current_thread().name, x))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

# 创建两个线程
print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
c = threading.Thread(target=check, name='checkThread')
t.start()
c.start()
t.join()
c.join()
print('thread %s is ended.' % threading.current_thread().name)



