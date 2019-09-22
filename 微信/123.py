# coding=utf-8
# 作者    ： Administrator
# 文件    ：123.py
# IED    ：PyCharm
# 创建时间 ：2019/9/21 13:54


a = '急售急售哈哈哈哈哈打傻了接口返回'

def key_words(word):
    """
    效验关键词
    :param word:
    :return:
    """
    with open('关键词.txt', 'r') as f:
        cons = f.readlines()
        cons = [i.replace('\n', '') for i in cons]
    for i in cons:
        if i in word:
            return True
    return False


key_words(a)