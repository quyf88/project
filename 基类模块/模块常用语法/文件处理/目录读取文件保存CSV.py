# -*- coding: utf-8 -*-
# @Time    : 2019/8/29 11:57
# @Author  : project
# @File    : 123.py
# @Software: PyCharm
import os
import shutil
"""基础操作"""
# 获取当前目录
path = os.getcwd()
# 返回指定目录下所有文件
files = os.listdir(path + r'/完成/')
# 筛选指定文件
files = [i for i in files if 'txt' in i if '备份数据' not in i]

for file_name in files:
    # 分割文件名和后缀
    (filename, extension) = os.path.splitext(file_name)
    new_file_name = filename + '.csv'
    print('新文件名：{}'.format(new_file_name))
    # 备份
    shutil.copy(file_name, '备份数据.xlsx')
    # 移动文件
    shutil.move(new_file_name, '完成/')
    # 删除文件
    os.remove(file_name)
    print('文件：{} 保存成功!'.format(new_file_name))

"""清空文件"""
with open('ExportFile/FriendValidation.txt', 'w') as f:
    f.seek(0)  # 光标移动至文件开头
    f.truncate()  # 清空文件
    print('获取记录清空成功')


"""文件保存为csv"""
import csv
def sav_data(self, data):
    """
    保存数据
    :return:
    """
    with open(self.file_name, "a+", encoding='utf-8', newline="") as f:
        k = csv.writer(f, delimiter=',')
        with open(self.file_name, "r", encoding='utf-8', newline="") as f1:
            reader = csv.reader(f1)
            if not [row for row in reader]:
                k.writerow(
                    ['行政区域', '项目名称', '项目位置', '土地用途', '行业分类', '面积(公顷)', '供地方式', '土地使用年限', '成交价(万元)', '约定容积率', '合同签订日期',
                     '数据来源', '数据写入日期'])
                k.writerows(data)
            else:
                k.writerows(data)