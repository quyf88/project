import pymysql


class MySql:
    def __init__(self):
        db_config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'qwe123',
            'db': 'news',
            'charset': 'utf8'
        }
        """获取连接对象和执行对象"""
        self.conn = pymysql.connect(**db_config)

    def create(self, content):
        """数据写入"""

        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 执行SQL操作

                sql = 'insert into words(keyword,new_url,new_tag,new_summary,source) VALUES ' \
                      '(%(keyword)s,%(url)s,%(tag)s,%(summary)s,%(source)s)'
                affectedcount = cursor.execute(sql, content)

                print('成功插入{0}条数据'.format(affectedcount))

                # 提交数据库事务
                self.conn.commit()

                # with代码块结束 关闭游标
        except pymysql.DatabaseError as e:
            # 回滚数据库事物
            self.conn.rollback()
            print('插入数据失败:{}'.format(e))
        finally:
            # 关闭数据连接
            self.conn.close()

    def find_db(self, sql):
        """数据查询"""
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 执行SQL操作
                cursor.execute(sql)
                # 提取结果集
                result_set = cursor.fetchall()
        finally:
            # 关闭数据连接
            self.conn.close()

        return result_set
