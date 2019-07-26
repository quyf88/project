# coding=utf-8
# 作者    ： Administrator
# 文件    ：Main_PIPE.py
# IED    ：PyCharm
# 创建时间 ：2019/6/15 19:36

import TaoBaoLoginApi
import sys


def main():

    # 如果不能实时输出打印信息 flush 刷新
    # sys.stdout.write('')
    # sys.stdout.flush()
    # time.sleep(2)
    a = TaoBaoLoginApi.Spider()
    a.main()


if __name__ == '__main__':
    main()

