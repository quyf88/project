# -*- coding:utf-8 -*-
# 文件 ：一条一条读取文档内容.py
# IED ：PyCharm
# 时间 ：2020/3/5 0005 15:49
# 版本 ：V1.0


for line in open("文档.txt", 'r', encoding='utf-8'):
    print(line)  # 一次提取一条
