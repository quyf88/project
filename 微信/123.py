# coding=utf-8
# 作者    ： Administrator
# 文件    ：123.py
# IED    ：PyCharm
# 创建时间 ：2019/8/24 18:34

# import re
#
# a = '2017款阿斯顿发的说法'
#
# b = re.findall(r'款(.*?)$',a)
# print(b)
#
# import random
# import datetime
#
# print(random.randint(10000, 99999))
# date = '今'
# date = date if date != '今天' else datetime.datetime.now().strftime('%d')
# print(date)

import datetime
release = '昨天'
if release == '今天':
    release = datetime.datetime.now().strftime('%m,%d')
elif release == '昨天':
    release = (datetime.datetime.now()+datetime.timedelta(days=-1))
    release = release.strftime('%m,%d')
print(release)

old_time = datetime.datetime.strptime('2019,' + release, '%Y,%m,%d')
new_time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y,%m,%d'), '%Y,%m,%d')
print(int((new_time-old_time)).days())


# a = datetime.datetime.strptime('2019年8月24', '%Y年%m月%d')
# b = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y,%m,%d'), '%Y,%m,%d')
#
# print(a, b)
# c = b-a
# print(c.days)

# import re
#
#
# a = '<android.widget.TextView index="0" text="8月"'
#
# print(re.findall(r'<android.widget.TextView index="." text="(.*?)"', a))






