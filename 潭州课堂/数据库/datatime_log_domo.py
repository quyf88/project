# coding=utf-8
# 作者    ： Administrator
# 文件    ：datatime_log_domo.py
# IED    ：PyCharm
# 创建时间 ：2019/6/1 12:54

import logging
from datetime import datetime

"""
1.写一个程序能接收用户输入出生日期从而计算出用户活了多久
2.使用logging模块化组件实现能记录错误信息到文件的程序，并在程序里制造错误，看错误信息是否被记录下来
"""

class A:

    def my_logging(self):
        m_log = logging.Logger('错误日志')
        mh = logging.FileHandler('m_log.log')
        mh.setLevel(logging.INFO)
        fmt = logging.Formatter('时间：%(asctime)s 文件名：%(filename)s 行号%(lineno)d')

        mh.setFormatter(fmt)
        m_log.addHandler(mh)

        return m_log

    def life_long(self, birthday):

        try:
            now = datetime.now()
            end = datetime.strptime(birthday, '%Y-%m-%d')
            days = now - end
            return days.days
        except Exception as e:
            self.my_logging().exception()
            log = self.my_logging()
            log.error(e)
            # 输出详细错误信息
            log.exception(e)


if __name__ == '__main__':
    day = life_long(input('请输入出生日期：年-月-日'))
    print('你总共活了{}天'.format(day))
