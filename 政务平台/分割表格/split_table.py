# coding=utf-8
# 作者    ： Administrator
# 文件    ：split_table.py
# IED    ：PyCharm
# 创建时间 ：2019/8/14 18:58
import pandas as pd

"""
根据行数拆分一个表格为多个表格
"""
filename = '2019年8月11.xlsx'
data = pd.read_excel(filename)
# 获取行数 shape[1]获取列数
rows = data.shape[0]

for num in range(1, 7):
    if num == 1:
        strat = 501
        end = rows
        name = '0-500'
    elif num == 2:
        strat = 0
        end = 501
        name = '501-1001'
    elif num == 3:
        strat = 0
        end = 1002
        name = '1001-1501'
    elif num == 4:
        strat = 0
        end = 1503
        name = '1501-2001'
    elif num == 5:
        strat = 0
        end = 2004
        name = '2001-2501'
    elif num == 6:
        strat = 0
        end = 2505
        name = '2501-'
    if strat > rows or end > rows:
        exit()
    # print(strat, end, num)
    count = 1
    while True:
        for i in range(strat, end):
            # drop 删除一行数据 inplace=True在原有表格修改
            data.drop(data.index[[strat]], inplace=True)
            rows1 = data.shape[0]
        # print(rows1)
        if num != 1 and num != 6:
            if count >= 2:
                break
            strat = 501
            end = rows1
            # print(strat, end, num)
            count += 1
            continue
        break
    data.to_excel("{}.xlsx".format(name), index=False, header=True)
    data = pd.read_excel(filename)


