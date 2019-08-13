import pandas as pd
import numpy as np

phone = 0

def read_xls():
    """
    读取 XLS表格数据
    :return:
    """
    # 加载数据
    df_read = pd.read_excel(r'a.xlsx')
    df = pd.DataFrame(df_read)
    # 获取指定表头的列数
    phone_num = 0  # 电话列
    name_num = 0  # 企业名称列
    code_num = 0  # 统一社会信用代码列
    type_num = 0  # 企业类型列
    for i in range(len(df.keys())):
        if df.keys()[i] == '电话':
            phone_num = i
        elif df.keys()[i] == '企业名称':
            name_num = i
        elif df.keys()[i] == '统一社会信用代码':
            code_num = i
        elif df.keys()[i] == '企业类型':
            type_num = i
    print(name_num, code_num, type_num, phone_num)
    # 循环每一行
    for indexs in df.index:
        #  fillna(0)将该列nan值修改为0 方便后续判断
        df.ix[indexs] = df.ix[indexs].fillna(0)
        # 读取指定行列数据 df.ix[行,列]
        data1 = df.ix[indexs, phone_num]
        # 修改指定单元格数据df.iloc[行, 列]
        if data1:
            print('有值')
            continue

        print('没有值')
        pre_name = df.ix[indexs, name_num]
        pre_code = df.ix[indexs, code_num]
        pre_type = df.ix[indexs, type_num]
        yield (pre_name, pre_code, pre_type)
        df.iloc[indexs, phone_num] = 123
        df.to_excel('a.xlsx', sheet_name='data', index=False, header=True)
        # 保存 sheet_name工作表名 index是否添加索引 header表头
        df.to_excel('a.xlsx', sheet_name='data', index=False, header=True)


datas = read_xls()
for pre_name, pre_code, pre_type in datas:

    print(pre_name, pre_code, pre_type)
