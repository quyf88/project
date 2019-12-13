# -*- coding:utf-8 -*-
# 文件 ：4.py
# IED ：PyCharm
# 时间 ：2019/12/13 0013 15:20
# 版本 ：V1.0


import os
from selenium import webdriver

'''
    第四步，浏览器执行第二步生成的html文件，抓取执行结果，保存到本地。
'''


class Crack:
    def __init__(self):
        self.browser = webdriver.Chrome()


if __name__ == "__main__":
    lists = os.listdir("newhtml/")
    crack = Crack()
    for fil in lists:
        file = os.path.exists("content/" + fil)
        if file:
            print('文件已经解析。。。' + str(file))
            continue
        print(fil)
        crack.browser.get(os.getcwd() + os.sep + "/newhtml/" + fil + "")
        text = crack.browser.find_element_by_tag_name('body')
        print(text.text)
        f = open("content/" + fil, "a", encoding="utf-8")
        f.write(text.text)
    else:
        f.close()
        crack.browser.close()
