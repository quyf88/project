"""检查数据是否更新  MD5模块"""
import hashlib
import os

from com.baiduwords.base_dao import BaseDao


class Md5Dao(BaseDao):
    def __init__(self):
        super().__init__()

    def dateupdate(self, data):
        """验证数据是否更新，更新返回True，未更新返回False"""

        # 创建md5对象
        md5obj = hashlib.md5()
        md5obj.update(data.encode(encoding='utf-8'))
        md5code = md5obj.hexdigest()
        print(md5code)

        old_md5code = ''
        f_name = 'md5.txt'

        if os.path.exists(f_name):  # 如果文件存在读取文件内容
            with open(f_name, 'r', encoding='utf-8') as f:
                old_md5code = f.read()

        if md5code == old_md5code:
            print('数据没有更新')
            return False
        else:
            # 把新的md5码写入到文件中
            with open(f_name, 'w', encoding='utf-8') as f:
                f.write(md5code)
            print('数据更新')
            return True




