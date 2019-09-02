# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 10:58
# @Author  : project
# @File    : 123.py
# @Software: PyCharm
import os
import logging


def main():
    with open('url.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            url = i.split()[0]            
            print(url)


if __name__ == '__main__':
    main()