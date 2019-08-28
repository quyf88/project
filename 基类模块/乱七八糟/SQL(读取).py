"""数据库读取数据管理DAO"""
from yingping.maoyan.base_dao import BaseDao


class DataBase(BaseDao):
    def __init__(self):
        super().__init__()

    def create(self, sql):
        """从数据库读取数据"""

        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 执行SQL操作
                cursor.execute(sql)
                # 提取结果集
                result_set = cursor.fetchall()

        finally:
            # 关闭数据连接
            self.close()

        return result_set




