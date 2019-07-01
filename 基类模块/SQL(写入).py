"""数据写入管理DAO"""

import pymysql
from com.baiduwords.base_dao import BaseDao


class FeedDao(BaseDao):
    def __init__(self):
        super().__init__()

    def create(self, feedbackword):
        """数据写入"""

        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 执行SQL操作
                sql = 'insert into HistoricalQuote ' \
                      '(Hfqjg,Tdate,Close,Zdf,Zdf3,Zdf5,Zdf10,AGSZBHXS, ' \
                        'Rzye,Rzyezb,Rzmre,Rzmre3,Rzmre5,Rzmre10,Rzche,Rzche3, ' \
                        'Rzche5,Rzche10,Rzjmre,Rzjmre3,Rzjmre5,Rzjmre10,Rqye,Rqyl, ' \
                        'Rqmcl,Rqmcl3,Rqmcl5,Rqmcl10,Rqchl,Rqchl3,Rqchl5,Rqchl10, ' \
                        'Rqjmcl,Rqjmcl3,Rqjmcl5,Rqjmcl10,Rzrqye,Rzrqyec,Sname)' \
                      ' values (%(hfqjg)s,%(tdate)s,%(close)s,%(zdf)s,%(zdf3)s,%(zdf5)s,%(zdf10)s,%(AGSZBHXS)s, ' \
                        '%(rzye)s,%(rzyezb)s,%(rzmre)s,%(rzmre3)s,%(rzmre5)s,%(rzmre10)s,%(rzche)s,%(rzche3)s, ' \
                        '%(rzche5)s,%(rzche10)s,%(rzjmre)s,%(rzjmre3)s,%(rzjmre5)s,%(rzjmre10)s,%(rqye)s,%(rqyl)s, ' \
                        '%(rqmcl)s,%(rqmcl3)s,%(rqmcl5)s,%(rqmcl10)s,%(rqchl)s,%(rqchl3)s,%(rqchl5)s,%(rqchl10)s, ' \
                        '%(rqjmcl)s,%(rqjmcl3)s,%(rqjmcl5)s,%(rqjmcl10)s,%(rzrqye)s,%(rzrqyec)s,%(sname)s)'

                affectedcount = cursor.execute(sql, feedbackword)
                print('成功插入{0}条数据'.format(affectedcount))

                # 提交数据库事务
                self.conn.commit()

                # with代码块结束 关闭游标
        except pymysql.DatabaseError as e:
            # 回滚数据库事物
            self.conn.rollback()
            print('插入数据失败' + e)
        finally:
            # 关闭数据连接
            self.conn.close()
