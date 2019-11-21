# -*- coding:utf-8 -*-
# 文件 ：MDB数据库操作.py
# IED ：PyCharm
# 时间 ：2019/11/21 0021 10:21
# 版本 ：V1.0

import pyodbc  # 导入pyodbc模块


# 数据库文件
DBfile = r"./area.mdb"
# 连接数据库.mdb文件
conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile)
# 创建游标对象
cursor = conn.cursor()

# 打印数据库goods.mdb中的所有表的表名
print('打印mdb数据库中的所有表的表名')
for table_info in cursor.tables(tableType='TABLE'):
    print(table_info.table_name)

# SQL：可执行的sql语句；tablename：要查询的表名,表名加中括号，以防表名中有空格
SQL = 'SELECT * FROM [area];'
# 获取所有查询的所有记录
# rows = cursor.execute(SQL).fetchall()
# 获取第一条数据
rows = cursor.execute(SQL).fetchone()
print(rows)
# 获取最后一条数据
new_rows = cursor.execute('SELECT * FROM [area] order by id desc;').fetchone()
print(new_rows)

# 提交数据（只有提交之后，所有的操作才会对实际的物理表格产生影响）
cursor.commit()  # 提交数据
cursor.close()  # 关闭游标
conn.close()  # 关闭数据库