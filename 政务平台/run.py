# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 8:53
# @Author  : project
# @File    : run.py
# @Software: PyCharm
"""多线程启动"""
import os
import time
import threading


# def say_hello(num):
#     print("Hello world!")
#     os.system('python server{}/spider.py'.format(num))
#
#
# def main():
#     for i in range(1):
#         thread = threading.Thread(target=say_hello, args=str(i+1))
#         thread.start()
#         time.sleep(10)
#
#
# main()
import pandas as pd
data = pd.read_excel("1.xlsx")
rows = data.shape[0]  # 获取行数 shape[1]获取列数

for num in range(1, 7):
    if num == 1:
        # 1 保留0-100
        strat = 101
        end = rows
        name = '0-100'
    elif num == 2:
        # 2 保留101-201
        strat = 0
        end = 101
        name = '101-201'
    elif num == 3:
        # 3 保留201-301
        strat = 0
        end = 202
        name = '201-301'
    elif num == 4:
        # 4 保留301-401
        strat = 0
        end = 303
        name = '301-401'
    elif num == 5:
        # 5 保留401-501
        strat = 0
        end = 404
        name = '401-501'
    elif num == 6:
        # 6 保留501-600
        strat = 0
        end = 505
        name = '501-'
    if strat > rows or end > rows:
        exit()
    # print(strat, end, num)
    count = 1
    while True:
        for i in range(strat, end):
            data.drop(data.index[[strat]], inplace=True)
            rows1 = data.shape[0]
        # print(rows1)
        if num != 1 and num != 6:
            if count >= 2:
                break
            strat = 101
            end = rows1
            # print(strat, end, num)
            count += 1
            continue
        break
    data.to_excel("{}.xls".format(name), index=False, header=True)
    data = pd.read_excel("1.xlsx")




# for i in istack_list:
#     new_df = pd.DataFrame()
#     new_df.to_excel("{}.xls".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')), index=False)
#
# # for indexs in data.index:
# #     print(data.iloc[indexs].values)
# #     print(indexs)

