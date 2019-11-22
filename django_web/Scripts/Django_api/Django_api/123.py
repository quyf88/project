# -*- coding:utf-8 -*-
# 文件 ：123.py
# IED ：PyCharm
# 时间 ：2019/11/22 0022 12:33
# 版本 ：V1.0

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "chenxiaoli2013", "access", charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()

print(data)

# 关闭数据库连接
db.close()
