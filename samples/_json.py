
# Python语言特定的序列化模块是pickle，
# 但如果要把序列化搞得更通用、更符合Web标准，就可以使用json模块


# -----序列化的标准格式：JSON---------
# 如果我们要在不同的编程语言之间传递对象，就必须把对象序列化为标准格式，比如XML，
# 但更好的方法是序列化为JSON，因为JSON表示出来就是一个字符串，
# 可以被所有语言读取，也可以方便地存储到磁盘或者通过网络传输。
# JSON不仅是标准格式，并且比XML更快，而且可以直接在Web页面中读取，非常方便
#
# Python内置的json模块提供了非常完善的Python对象到JSON格式的转换

import json  # 注:如果文件名定义为json.py,则引用会默认为本文件，而非json库


class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score


# Student实例转为dict
def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }


# dict 转为Student实例
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])

# Student序列化为json格式
s = Student('Bob', 20, 88)
print(json.dumps(s, default=student2dict))
print(json.dumps(s, default=lambda obj: obj.__dict__))  # 把任意实例变为dict

# json反序列化为Student实例
json_str = '{"age":20, "score":88, "name":"Bob"}'
print(json.loads(json_str, object_hook=dict2student))

# ************************** 练习题 **********************
#   对中文进行JSON序列化时，json.dumps()提供了一个ensure_ascii参数
#   观察该参数对结果的影响
obj = dict(name='小明', age=20)
s1 = json.dumps(obj, ensure_ascii=True)
s2 = json.dumps(obj, ensure_ascii=False)
print(s1)
print(s2)

# s1输出结果： {"age": 20, "name": "\u5c0f\u660e"}
# s2输出结果： {"age": 20, "name": "小明"}
# 参数ensure_ascii使中文变为对应的 ascii码 了吗？
