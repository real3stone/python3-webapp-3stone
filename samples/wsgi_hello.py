# 【WSGI接口: web service gateway interface 】
# 封装TCP连接、HTTP原始请求和响应格式，使我们专心于Python编写web业务

# 其实一个web app可以理解为就是写一个WSGI的处理函数

# WSGI接口实现非常简单，只需要开发者实现一个函数即可响应HTTP请求
# 无论多么复杂的Web应用程序，入口都是一个WSGI处理函数。
# HTTP请求的所有输入信息都可以通过environ获得，
# HTTP响应的输出都可以通过start_response()加上函数返回值作为Body。

# **本代码是请求部分，server部分在wsgi_server.py中**


# 定义一个符合WSGI标准的HTTP处理函数，接受两个参数
# 【environ】：包含所有HTTP请求信息的dict对象
# 【start_response】: 发送HTTP响应 的 函数
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    # 从environ中读取PATH_INFO，默认值为web
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    # print('-------------------------------------------')
    print(environ)
    # print('-------------------------------------------')
    return [body.encode('utf-8')]

# 有了WSGI，我们关心的是如何从environ这个dict对象拿到HTTP请求信息，
# 然后构造HTML，通过start_response()发送Header，最后返回Body

# 整个application()函数没有涉及任何解析HTTP的部分，即底层代码不需要我们编写
# 只用负责考虑更高层次上如何响应请求

# 由于我们提供不了application()参数值，也不能接收返回的bytes
# 所有application()必须有WSGI服务器来调用

# 复杂的Web应用程序，光靠一个WSGI函数来处理还是太底层了，
# 我们需要在WSGI之上再抽象出Web框架，进一步简化Web开发。
