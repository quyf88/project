"""数据库读取数据管理DAO"""
from com.baiduwords.base_dao import BaseDao


class WordsIdDao(BaseDao):
    def __init__(self):
        super().__init__()

    def create(self):
        """从数据库读取关键词"""

        words = []

        try:
            # 2. 创建游标对象
            with self.conn.cursor() as cursor:
                # 3. 执行SQL操作
                sql = 'select Id,Words,WriteDate from WordsKey'
                cursor.execute(sql)
                # 4. 提取结果集
                result_set = cursor.fetchall()

                for row in result_set:
                    product = {}
                    product['Id'] = row[0]
                    product['Words'] = row[1]
                    product['WriteDate'] = row[2]
                    words.append(product['Words'])
                # with代码块结束 5. 关闭游标
        finally:
            # 6. 关闭数据连接
            self.close()

        return words


