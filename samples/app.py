# 【web框架--Flask】

# WSGI提供的接口虽然比HTTP接口高级了不少，
# 但和Web App的处理逻辑比，还是比较低级，我们需要在WSGI接口之上能进一步抽象，
# 让我们专注于用一个函数处理一个URL，至于URL到函数的映射，就交给Web框架来做

# Flask通过Python的<装饰器>在内部自动地把URL和函数关联起来


# 处理3个URL：
# GET /: 首页，返回Home
# GET/signin: 登录页，显示登录表单
# POST /signin: 处理登录表单，显示登录结果

# 同一个URL /signin 分别有GET和POST两种请求，映射到两个处理函数
from flask import Flask
from flask import request

app = Flask(__name__)   # 定义一个flask框架对象


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'


@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post"
              <p><input name="username"></p>
              <P><input name="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''


@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    # Web框架都提供了自己的API来实现从请求拿到用户数据,Flask通过request.form['name']来获取表单的内容
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return '<h3>Hello, admin!</h3>'
    # 实际的Web App应该拿到用户名和口令后，去数据库查询再比对，来判断用户是否能登录成功

if __name__ == '__main__':
    app.run()


# 有了Web框架，我们在编写Web应用时，注意力就从<WSGI处理函数>转移到<URL+对应的处理函数>
# 在编写URL处理函数时，除了配置URL外，从HTTP请求拿到用户数据也是非常重要的。
# Web框架都提供了自己的API来实现这些功能。【Flask】通过request.form['name']来获取表单的内容


# 在函数中返回一个包含HTML的字符串，简单的页面还可以，但是复杂页面还用python字符串表示很困难
# 下一步我们需要把html和Python代码分离开来，提升web开发的效率 --> 模板
