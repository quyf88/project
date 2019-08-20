# -*- coding: utf-8 -*-
# @Time    : 2019/8/20 14:36
# @Author  : project
# @File    : 合并表格.py
# @Software: PyCharm
import os
import xlwt
import xlrd
import datetime
# 表头
biaotou = ['企业名称', '经营状态',	'法定代表人',	'注册资本', '成立日期',	 '所属省份',
           '所属城市', '电话', '身份证号码', '邮箱', '统一社会信用代码', '纳税人识别号',
           '注册号', '组织机构代码', '企业类型', '所属行业',	'网址', '企业地址', '经营范围']
# 读取出全部文档
path = os.getcwd()
files = os.listdir(path)
files = [i for i in files if '.xlsx' in i]
print("在默认文件夹下有%d个文档" % len(files))
matrix = [None]*len(files)
# 实现读写数据
# 将所有文件读数据到三维列表cell[][][]中（不包含表头）
for i in range(len(files)):
    bk = xlrd.open_workbook(files[i])
    try:
        sh = bk.sheet_by_name("data")
    except:
        print("在文件%s中没有找到sheet1，读取文件数据失败,要不你换换表格的名字？" % files[i])
        continue
    nrows = sh.nrows
    matrix[i] = [0] * (nrows - 1)
    ncols = sh.ncols
    for m in range(nrows - 1):
        matrix[i][m] = ["0"] * ncols
    for j in range(1, nrows):
        for k in range(0, ncols):
            matrix[i][j - 1][k] = sh.cell(j, k).value

# 写数据到新的表格
filename = xlwt.Workbook()
sheet = filename.add_sheet("hel")
# 写入表头
for i in range(len(biaotou)):
    sheet.write(0, i, biaotou[i])
# 求和前面的文件一共写了多少行
count = 1
for i in range(len(files)):
    for j in range(len(matrix[i])):
        for k in range(len(matrix[i][j])):
            sheet.write(count, k, matrix[i][j][k])
        count += 1
new_file_name = datetime.datetime.now().strftime('%Y-%m-%d') + '完成.xlsx'
print("我已经将%d个文件合并成1个文件，并命名为%s快打开看看正确不？" % (len(files), new_file_name))
filename.save(new_file_name)
