# 【子进程】


# subprocess模块可以让我们非常方便地启动一个子进程，然后控制器输入输出
import subprocess

# 演示如何在Python代码中运行命令 nslookup www.python.org
print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code:', r)


# 如果子进程还需要输入，则可以通过communicate()方法输入：
print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)

# 输出有问题，显示utf-8不能decode
