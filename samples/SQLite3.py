# -*- coding: utf-8 -*-
# 【数据库】练习

# SQLite3是Python内置的数据库，SQLite的特点是轻量级、可嵌入，
# 但不能承受高并发访问，适合桌面和移动应用
import os
import sqlite3


db_file = os.path.join(os.path.dirname(__file__), 'test.db')

if os.path.isfile(db_file):
    os.remove(db_file)

# 初始数据：
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
cursor.close()
conn.commit()
conn.close()


def get_score_in(low, high):
    # 返回指定分数区间的名字，按分数从低到高排序
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(r'select * from user where score >= ? and score <= ? order by score', (low, high))
        values = cursor.fetchall()
        name = [i[1] for i in values]  # tuple操作--取出第二个元素组成list
    except Exception as e:
        print(e)
    finally:
        cursor.close()  # 关闭数据库
        conn.close()
    print(name)  # 输出查询结果
    return name


# 测试
assert get_score_in(80, 95) == ['Adam']
assert get_score_in(60, 80) == ['Bart', 'Lisa']
assert get_score_in(60, 100) == ['Bart', 'Lisa', 'Adam']

print('Pass')  # 测试成功


# 由于Python的DB-API定义都是通用的，所以，操作MySQL的数据库代码和SQLite类似
# 1、把sqlite3 换成 mysql.connector
# 2、mysql的占位符是 %s，而非？



