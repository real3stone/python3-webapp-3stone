# 【IO编程】练习
from io import StringIO
from io import BytesIO

print('---------read --------------')

# 文件读写是可能会产生IOError
try:
    f = open('test.txt', 'r', encoding='utf-8-')
    print(f.read())
finally:
    if f:
        f.close()

print('----------use with-------------')

# 和前面的try...finally是一样的，但是更简洁，且不必调用f.close()方法
with open('test.txt', 'r', encoding='utf-8-') as f:
    print(f.read())

print('----------read lines-------------')

f = open('test.txt', 'r', encoding='utf-8-')
n = 1
for line in f.readlines():   # 按行读取
    print('line %d' % n, line.strip())   # 把末尾的'\n'删掉
    n += 1

print('----------write -------------')

# with open('test.txt', 'a') as f:
#     f.write('hello 3stone')
# 模式'a' = append 追加写入

print('----------String IO-----------')
# 内存中操作str
# 要读取StringIO，可以用str初始化StringIO，然后想读文件一样读取
f_str = StringIO('Hello!\nHi\nGoodbye!')
while True:
    s = f_str.readline()
    if s == '':
        break
    print(s.strip())

print('----------Bytes IO-----------')
# 内存中操作 bytes
# 与StringIO类似
f_byt = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
b = f_byt.read()
print(b.strip())

# ***********************操作文件&目录************************

# Python内置的os模块可以直接调用操作系统提供的接口函数
# Python的os模块封装了操作系统的目录和文件操作，
# 要注意这些函数有的在os模块中，有的在os.path模块中

# 练习题没有做！

# ************************* 序列化 ************************

# 把变量从内存中变成可存储或传输的过程称之为序列化(pickling)
# 把变量内容从序列化的对象重新读到内存里称之为反序列化(unpickling)


# -----序列化的标准格式：JSON---------
# 如果我们要在不同的编程语言之间传递对象，就必须把对象序列化为标准格式，比如XML，
# 但更好的方法是序列化为JSON，因为JSON表示出来就是一个字符串，
# 可以被所有语言读取，也可以方便地存储到磁盘或者通过网络传输。
# JSON不仅是标准格式，并且比XML更快，而且可以直接在Web页面中读取，非常方便
#
# Python内置的json模块提供了非常完善的Python对象到JSON格式的转换













