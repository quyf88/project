# -*- coding: utf-8 -*-
# @Time    : 2019/6/21 9:44
# @Author  : project
# @File    : MD5_Dao.py
# @Software: PyCharm

"""检查数据是否更新  MD5模块"""
import hashlib
import os


class Md5Dao:
    def dateupdate(self, path):
        """验证数据是否更新，更新返回True，未更新返回False"""

        # 创建md5对象
        md5obj = hashlib.md5()
        # 判断传入效验文件是否存在 不存在则创建
        if not os.path.exists(path):
            a = open(path, 'w', encoding='utf-8')
            a.close()
        # 传入文件路径 读取文件生成校验码
        with open(path, 'r', encoding='utf-8') as f:
            md5obj.update(f.read().encode(encoding='utf-8'))
            md5code = md5obj.hexdigest()
            # print(md5code)

        old_md5code = ''
        f_name = 'md5.txt'

        if os.path.exists(f_name):  # 如果文件存在读取文件内容
            with open(f_name, 'r', encoding='utf-8') as f:
                old_md5code = f.read()

        if md5code == old_md5code:
            # print('数据没有更新')
            return False
        else:
            # 把新的md5码写入到文件中
            with open(f_name, 'w', encoding='utf-8') as f:
                f.write(md5code)
            # print('数据更新')
            return True