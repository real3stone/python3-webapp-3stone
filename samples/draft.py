# 莫烦Python练习代码
import threading
import time
from queue import Queue


def job(l, q):
    for i in range(len(l)):
        l[i] **= 2
    return l


def thread_job():
    # print('This is a added Thread, number is %s' % threading.current_thread())
    print('T1 start\n')
    for i in range(10):
        time.sleep(0.1)
    print('T1 finish\n')


def T2_job():
    print('T2 start\n')
    print('T2 finish\n')


def main():
    added_thread = threading.Thread(target=thread_job, name='T1')
    thread2 = threading.Thread(target=T2_job )
    added_thread.start()
    thread2.start()
    thread2.join()
    added_thread.join()
    print('all done\n')
    # print(threading.active_count())
    # print(threading.enumerate())
    # print(threading.current_thread())


if __name__ == '__main__':
    main()
