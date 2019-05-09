# coding=utf-8
# 作者    ： Administrator
# 文件    ：文件操作.py
# IED    ：PyCharm
# 创建时间 ：2019/5/4 18:19


# 作业1 复制文件

# with open("123.html", "r", encoding='utf-8') as f:
#     with open("456.html", "w+", encoding="utf-8") as f1:
#         a = f.read()
#         f1.write(a)
#         f1.seek(0)
#         print(f1.read())

import os


def func(li):
    if os.path.isdir(li):
        directory = os.listdir(li)
        for i in directory:
            print(i)
    else:
        print("这不是一个文件夹")


if __name__ == '__main__':
    li = os.getcwd()
    func(li)

