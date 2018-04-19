# 编写底层模块的第一步：先把调用接口写出来

from orm import Model, StringField, IntegerField


# 父类Model和属性类型StringField、IntegerField都是由ORM框架提供的，剩下的魔术方法
# 如save()全部有metaclass自动完成
class User(Model):
    # 定义 类的属性 到 数据表列 的映射
    id = IntegerField('123')
    name = StringField('3stone')
    email = StringField('test@orm.org')
    password = StringField('999999')

# metaclass可以隐式地继承到子类，但子类自己却感觉不到
