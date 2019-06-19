# -*- coding: utf-8 -*-
# @Time    : 2019/6/19 16:12
# @Author  : project
# @File    : 123.py
# @Software: PyCharm

import send_sms


send_sms.send_sms(1, 2)

a = {'ReturnStatus': 'Success', 'Message': 'ok', 'RemainPoint': 7941, 'TaskID': 93096378, 'SuccessCounts': 1}
print(a['ReturnStatus'])
if a['RemainPoint'] > 8000:
    print(1)
else:
    print(2)