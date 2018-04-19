# 测试：ORM框架(使用metaclass编写)
from model import User

# 创建一个实例：
u = User(id=1234, name='3stone', email='test@orm.orm', password='password')
# 保存到数据库
u.save()
