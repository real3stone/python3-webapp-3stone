# 【WSGI：web service gateway interface】练习
# Python内置了一个WSGI服务器，这个模块叫<wsgiref>，
# 它是用纯Python编写的WSGI服务器的参考实现


# server部分代码

# 从wsgiref模块导入：
from wsgiref.simple_server import make_server
# 导入我们自己编写的application()函数
from wsgi_hello import application  # pycharm提示有错，但是命令行可以运行


# 创建一个服务器，IP地址为空，端口是8000，处理函数是application
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求：
httpd.serve_forever()


