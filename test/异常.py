# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 13:21
# @Author  : project
# @File    : 异常.py
# @Software: PyCharm

"""异常处理"""

f = open("123.html", "w")
print("打开文件")
try:
    f.write(b)
except Exception as e:
    print("写入错误")
finally:
    print("关闭文件")
    f.close()
