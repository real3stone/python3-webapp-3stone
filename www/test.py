# 测试ORM & models

import orm
from models import User, Blog, Comment
import asyncio
import mysql.connector


async def test(loop):
    db_dict = {'host': '127.0.0.1', 'post': '3306', 'user': 'root', 'password': '123456', 'database': 'awesome'}
    await orm.create_pool(loop=loop, **db_dict)
    # 没有设置默认值的一个也不能少
    u = User(name='Test', email='stone@mail.com', passwd='123456', image='about:blank')
    await u.save()
    await orm.destroy_pool()  # test结束，关闭mysql连接池 否则会报错
'''
# 插入User对象（不要重复插入同一email，因为它是unique key）

# 获取EventLoop：
loop = asyncio.get_event_loop()
# 把协程丢到EventLoop中执行
loop.run_until_complete(test(loop))
# 关闭EventLoop
loop.close()
'''

'sql check code'
conn = mysql.connector.connect(user='root', password='123456', database='awesome')

cursor = conn.cursor()
cursor.execute('select * from users')
data = cursor.fetchall()
for x in data:
    print(x)



