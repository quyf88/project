# coding=utf-8
# 作者    ： Administrator
# 文件    ：表格切割.py
# IED    ：PyCharm
# 创建时间 ：2019/8/14 18:58
import pandas as pd

"""
根据行数拆分一个表格为多个表格
"""
# 拆分个数
nums = 15

filename = '深圳培训企业信息.xls'
data = pd.read_excel(filename)
# 获取行数 shape[1]获取列数
rows = data.shape[0]

for num in range(nums):
    if num == 0:
        strat = 501
        end = rows
        name = num
    else:
        strat = 0
        end = num * 501
        name = num
        print(strat, end)

    if strat > rows or end > rows:
        exit()

    count = 1
    while True:
        for i in range(strat, end):
            # drop 删除一行数据 inplace=True在原有表格修改
            data.drop(data.index[[strat]], inplace=True)
            rows1 = data.shape[0]
        # print(rows1)
        if num != 0:
            if count >= 2:
                break
            strat = 501
            end = rows1
            count += 1
            continue
        break
    data.to_excel("{}.xlsx".format(name), index=False, header=True)
    print('文件：[{}.xlsx]分割成功'.format(name))
    data = pd.read_excel(filename)


