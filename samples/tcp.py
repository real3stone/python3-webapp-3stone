# 【TCP编程】

# 导入socket库
import socket


# 创建一个socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接
s.connect(('www.sina.com.cn', 80))


# 发送请求数据：
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

# 接收数据
buffer = []
while True:  # 反复接收，直到recv()返回空数据
    # 每次最多接受1k字节：
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)

# 关闭连接
s.close()

# 收到的数据包括HTTP头和网页本身，需分离HTTP头和网页
# 把HTTP头打印一下，网页内容保存到文件
header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))
# 把接受的数据写入文件
with open('sina.html', 'wb') as f:
    f.write(html)







