# 测试ORM & models

import orm
from models import User, Blog, Comment
import asyncio
import mysql.connector


async def test(loop):
    db_dict = {'host': '127.0.0.1', 'post': '3306', 'user': 'root', 'password': '123456', 'database': 'awesome'}
    await orm.create_pool(loop=loop, **db_dict)
    # 没有设置默认值的一个也不能少
    u = User(name='Test', email='32stone@mail.com', passwd='123456', image='about:blank')
    '''
    u = User()
    u.name = 'Test'
    u.email = 'stone@foxmail.com'
    u.passwd = '123456'
    u.image = 'about:blank'
    u.id = '123'
    '''
    await u.save()
    await orm.destroy_pool()  # test结束，关闭mysql连接池

# 获取EventLoop：
loop = asyncio.get_event_loop()

print('*********** 0 **************')

# 把协程丢到EventLoop中执行
loop.run_until_complete(test(loop))

# 关闭EventLoop
loop.close()

print('*********** 1 **************')

'sql check code'
conn = mysql.connector.connect(user='root', password='123456', database='awesome')

print('*********** 2 **************')

cursor = conn.cursor()
cursor.execute('select * from users')
data = cursor.fetchall()
print(data)



