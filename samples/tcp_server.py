# 【tcp server部分】

import socket
import threading
import time

# 建立连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定监听的地址和端口, 选9999这个端口1来实验
s.bind(('127.0.0.1', 9999))  # 绑定本机地址
# 监听端口
s.listen(5)
print('Waiting for connection....')


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcom!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)


while True:
    # 接受一个新连接：
    sock, addr = s.accept()
    # 创建 新线程 来处理TCP连接：
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()








