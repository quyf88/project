# -*- coding: utf-8 -*-
# @Time    : 2019/6/21 9:47
# @Author  : project
# @File    : 123.py
# @Software: PyCharm

import os
import re
q = '182108'
path = os.path.abspath('.') + '\log\send_sms.txt'
with open(path, 'a+', encoding='utf-8')as f:
    f.seek(0)
    a = [i.replace('\n', '') for i in f.readlines()]
    if q in a:
        print(1)
    else:
        f.write(q+'\n')



