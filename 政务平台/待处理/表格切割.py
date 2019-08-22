# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 13:16
# @Author  : project
# @File    : 表格切割.py
# @Software: PyCharm
import os
import xlwt
import xlrd


def separation(share):
    """
    将一个表格平均拆分为多个表格
    :return:
    """
    # 定义表头
    Head = ['企业名称', '经营状态',	'法定代表人',	'注册资本', '成立日期',	 '所属省份',
            '所属城市', '电话', '身份证号码', '邮箱', '统一社会信用代码', '纳税人识别号',
            '注册号', '组织机构代码', '企业类型', '所属行业',	'网址', '企业地址', '经营范围']
    # 读取出当前目录下全部文档
    path = os.getcwd()
    files = os.listdir(path)
    files = [i for i in files if '.xlsx' in i]
    print("在默认文件夹下有%d个文档" % len(files))

    # 将所有文件读数据到三维列表cell[][][]中（不包含表头）
    matrix = [None] * len(files)
    for i in range(len(files)):
        # 打开文档
        bk = xlrd.open_workbook(files[i])
        try:
            # print(bk.nsheets)  # 获取sheet总数
            # print(bk.sheet_names())  # 获取sheet名称列表
            # print(bk.sheet_by_index(0))  # 根据索引获取sheet
            # print(bk.sheet_by_name("data"))  # 根据sheet名称获取sheet
            sh = bk.sheet_by_index(0)
        except:
            print("在文件%s中没有找到sheet1，读取文件数据失败,要不你换换表格的名字？" % files[i])
            continue
        # 当前工作簿总行数
        nrows = sh.nrows
        print(nrows)
        matrix[i] = [0] * (nrows - 1)
        # 当前工作簿总列数
        ncols = sh.ncols
        for m in range(nrows - 1):
            matrix[i][m] = ["0"] * ncols
        for j in range(1, nrows):
            for k in range(0, ncols):
                matrix[i][j - 1][k] = sh.cell(j, k).value
        # 计算表格数
        end_num = int(nrows / share) + 1
        print(end_num)
    # 写数据到新的表格
    for number in range(end_num):
        filename = xlwt.Workbook()
        sheet = filename.add_sheet("data")
        # 写入表头
        for i in range(len(Head)):
            sheet.write(0, i, Head[i])
        if number == 0:
            strat = 0
            end = share
        else:
            strat = share * number
            end = share * (number+1)

        if strat > nrows or end > nrows:
            strat = share * number
            end = nrows-1
        # 求和前面的文件一共写了多少行
        print(strat, end)
        count = 1
        for i in range(len(files)):
            for j in range(strat, end):
                for k in range(len(matrix[i][j])):
                    sheet.write(count, k, matrix[i][j][k])
                count += 1

        # 合并后文件名
        new_file_name = str(number) + '.xlsx'
        # 保存合并后文件
        filename.save(new_file_name)
        print("我已经将文件拆分成1个文件，并命名为{}快打开看看正确不？".format(new_file_name))


if __name__ == '__main__':
    # share 分割表格数据数量
    separation(share=130)