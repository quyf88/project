# coding=utf-8
# 作者    ： Administrator
# 文件    ：mysql_conn.py
# IED    ：PyCharm
# 创建时间 ：2019/6/19 22:43


import pymysql


class BaseDao(object):
    def __init__(self):

        self.coon = pymysql.connect(host="localhost", user="root", password="raspberry", db="news", port=3306)

    def add_update_del_seek(self, content):

        try:
            with self.coon.cursor() as cursor:
                # count的是影响的行数
                sql = "insert into words(symbol,nam,trade,pricechange,changepercent,buy,sell,settlement,opens,high,low,volume,amount)" \
                      " values(%(symbol)s,%(name)s,%(trade)s,%(pricechange)s,%(changepercent)s,%(buy)s,%(sell)s,%(settlement)s,%(opens)s,%(high)s,%(low)s,%(volume)s,%(amount)s)"

                count = cursor.execute(sql, content)
                self.coon.commit()
                """
                fetchall 返回所有的查询结果 fetchone只返回一条查询的结果 这里选用fetchall 
                当然你也可以用fetchone但它最多只返回一条查询语句
                """
                # 如果是增删改的话，返回的结果是一个元组，如果是查的话返回的结果是一个嵌套的元组
                print("成功插入：{}条数据".format(count))
                # return count

        except Exception as e:
            print(e)
            self.coon.rollback()
        finally:
            self.coon.close()













