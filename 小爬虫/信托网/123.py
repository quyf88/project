# -*- coding:utf-8 -*-
# 文件 ：script.py
# IED ：PyCharm
# 时间 ：2020/2/13 0013 21:55
# 版本 ：V1.0


def read_id():
    """读取产品ID"""
    with open('a.txt', 'r', encoding='utf-8') as f:
        contents = [i.replace('\n', '') for i in f.readlines()]
        for content in contents:
            content = content.split(',')[1]
            yield content


if __name__ == '__main__':
    # read_id()
    # for i in read_id():
    #     print(i)
    name = [1]
    name = name[0] if name else '11111'
    print(name)