# UDP 服务器部分
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定端口
s.bind(('127.0.0.1', 9999))

# 不需要listen()方法，直接接受来自客户端的数据

print('Bind UDP on 9999...')
while True:
    # 接受数据
    data, addr = s.recvfrom(1024)
    print('Received %s:%s.' % addr)  # 打印地址&端口
    s.sendto(b'Hello, %s!' % data, addr)


