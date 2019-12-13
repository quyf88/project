# -*- coding:utf-8 -*-
# 文件 ：3.py
# IED ：PyCharm
# 时间 ：2019/12/13 0013 15:16
# 版本 ：V1.0


import os
import re

'''
第三步 解析出每个车型的数据json，保存到本地。
'''
if __name__ == "__main__":
    print("Start...")
    rootPath = "html/"
    files = os.listdir(rootPath)
    for file in files:
        print("fileName==" + file.title())
        text = ""
        for fi in open(rootPath + file, 'r', encoding="utf-8"):
            text = text + fi
        else:
            print("fileName==" + file.title())
        # 解析数据的json
        jsonData = ""
        config = re.search('var config = (.*?){1,};', text)
        if config != None:
            print(config.group(0))
            jsonData = jsonData + config.group(0)
        option = re.search('var option = (.*?)};', text)
        if option != None:
            print(option.group(0))
            jsonData = jsonData + option.group(0)
        bag = re.search('var bag = (.*?);', text)
        if bag != None:
            print(bag.group(0))
            jsonData = jsonData + bag.group(0)
        color = re.search('var color = (.*?);', text)
        if color != None:
            print(color.group(0))
            jsonData = jsonData + color.group(0)
        innerColor = re.search('var innerColor = (.*?);', text)
        if innerColor != None:
            print(innerColor.group(0))
            jsonData = jsonData + innerColor.group(0)
        # print(jsonData)
        f = open("json/" + file, "a", encoding="utf-8")
        f.write(jsonData)
        f.close()
