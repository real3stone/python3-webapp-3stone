# 【模板model】练习

# 使用模板，我们需要预先准备一个HTML文档，这个HTML文档不是普通的HTML，
# 而是 嵌入了一些变量和指令，然后，根据我们传入的数据，<替换>后，得到最终的HTML，发送给用户

# Flask通过 render_template()函数 来实现模板渲染。
# Flask默认支持的模板是：Jinja2

from flask import Flask, request, render_template


app = Flask(__name__)


# 专注于一个函数处理一个URL，URL到函数的映射就交给web框架来做
# 即：Flask中定义的装饰器app.route()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')  # render_template()


@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'password':
        return render_template('sign-ok.html', username=username)
    else:
        return render_template('form.html', message='Bad username or password', username=username)

if __name__ == '__main__':
    app.run()  # 运行后，Flask框架自带的server会在端口5000监听



