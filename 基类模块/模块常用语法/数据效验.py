# coding=utf-8
# 作者    ： Administrator
# 文件    ：数据效验.py
# IED    ：PyCharm
# 创建时间 ：2019/10/23 20:54
import hashlib


def make_file_id(src):
    """
    生成哈希MD5码
    :param src: 字符串
    :return:
    """
    m1 = hashlib.md5()
    m1.update(src.encode('utf-8'))
    return m1.hexdigest()


def friend_validation(make):
    """
    效验是否获取过该条推文信息
    :return:
    """
    with open('config/FriendValidation.txt', 'r') as f:
        flight = [i.replace('\n', '') for i in f.readlines()]
        if make in flight:
            return True
        with open('config/FriendValidation.txt', 'a+') as f1:
            f1.write(make)
            f1.write('\n')
        return False
