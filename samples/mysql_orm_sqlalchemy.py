# 【ORM:sqlalchemy】

# MySQL是为服务器端设计的数据库，能承受高并发访问，同时占用的内存也远远大于SQLite
# 此外，MySQL内部有多种数据库引擎，最常用的引擎是支持数据库事务的InnoDB


# 【ORM技术】：Object-Relational Mapping，把关系数据库的表结构映射到Python对象上
# 在Python中，最有名的<ORM框架>是SQLAlchemy

# ORM框架的作用就是把数据库表的<一行记录>与<一个对象>互相做自动转换
# 正确使用ORM的前提: 了解关系数据库的原理

# 导入SQLAlchemy并初始化DBSession
from sqlalchemy import Column, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


# 创建对象基类
Base = declarative_base()


# 定义User对象
class User(Base):
    # 表的名字：
    __tablename__ = 'user'
    # 表的结构：（类属性）
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # 一对多
    books = relationship('Book')


# 定义Book对象 (后边没有调用)
class Book(Base):
    __tablename__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # “多”的一方的book表示通过外键user.id关联到user表的：
    user_id = Column(String(20), ForeignKey('user.id'))
    # 当我们查询一个User对象时，该对象的books属性将返回一个包含若干个Book对象的list


# 初始化数据库连接：
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/test')
# 创建DBSession对象(数据库会话)，可视为当前数据库连接：
DBSession = sessionmaker(bind=engine)  # bind:会话关联数据库连接engine


# 插入操作只能执行一次
"""
# 由于有了ORM，我们想数据库表中添加一行记录，可以视为添加一个user对象：

# 创建session对象
session = DBSession()
# 创建User对象：
new_user = User(id='5', name='Bob')
# 添加到session
session.add(new_user)
# 提交即保存到数据库
session.commit()
# 关闭session
session.close()

"""

# 查询：有了ORM，查询出来的可以不再是tuple,而是User对象

# 创建Session
session = DBSession()
# 创建Query查询， filter是where条件(过滤)，最后调用one()返回唯一行，
# 如果调用all()则返回所有行：
user = session.query(User).filter(User.id == '5').one()
# 打印类型和对象的name属性：
print('type:', type(user))
print('name:', user.name)
# 关闭Session
session.close()














