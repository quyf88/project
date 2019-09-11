# encoding: utf-8
# @Time: 
# @software: PyCharm
# @file: 根据文件名顺序排序.py
# @time: 2019/9/11 11:49

"""根据文件名顺序排序(数字)"""
import os
filelist = os.listdir('./')
for file in filelist:
    orgName = file
    file = file.split("_")
    if len(file[3]) < 7:
        for i in range(7-len(file[3])):
            file[3] = "0"+file[3]
        print(file)
        filename = "_".join(file)
        print(filename)
        os.rename(orgName, filename)
    else:
        pass
