# coding=utf-8
# 作者    ： Administrator
# 文件    ：123.py
# IED    ：PyCharm
# 创建时间 ：2019/6/15 17:01




import os

import subprocess
#
# os.system('TaoBaoLoginApi.py')

# output = subprocess.getstatusoutput('GUI.py')
# print(output)

# fp = os.popen('GUI.py')
# for line in iter(fp.readline, ''):
#     print(line, end='')
#     print(1)
import test
import subprocess
import sys

import sys
a = ''

# savedStdout = sys.stdout #保存标准输出流
#
# sys.stdout = a #标准输出重定向至文件
# print('This message is for file!')
# print(a)
# sys.stdout = savedStdout #恢复标准输出流
# print('This message is for screen!')

import shlex
import subprocess

if __name__ == '__main__':

    r = subprocess.Popen(['python', r'Main_PIPE.py'],  # 需要执行的文件路径
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         bufsize=1)
    while r.poll() is None:
        line = str(r.stdout.readline(), encoding='utf-8')
        line = line.strip()

        if line:
            print('Subprogram output: [{}]'.format(line))
    # if r.returncode == 0:
    #     print('Subprogram success')
    # else:
    #     print('Subprogram failed')

# fp = os.popen('Main_PIPE.py')
# for line in iter(fp.readline, ''):
#     print(line, end='')





# import requests
# import json
# url ='http://flight-api.tuniu.com/query/flight/v2/list?callback=jQuery172020007985488015922_1560600800021&{%22withTransfer%22:true,%22passengers%22:[{%22count%22:1,%22psgType%22:%22ADT%22}],%22voyType%22:%22ST%22,%22voys%22:[{%22orgCity%22:%22BJS%22,%22dstCity%22:%22SHA%22,%22deptDate%22:%222019-06-17%22}],%22tokenKey%22:%22G92ZWFuZHBlYWNlMmxpZ2h0L3YyL2xpc%22,%22useToken%22:true}&_=1560600800239'
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'}
#
#
# response = requests.get(url, headers=headers)
# a = response.text
#
# b = a.split('(')
# c = b[1].replace(")", '')
# data = (json.loads(c).get('data'))
# airComMap = data['airBasic']['airComMap']  # 航空公司
# airPortMap = data['airBasic']['airPortMap']  # 航班时间
# voyGroups = data['voyGroups']  # 航班详细信息
# for i in voyGroups:
#     print(airComMap)
#     print(airPortMap)
#     voys = i['voys'][0]['segFltKeys']  # 航班号 出发到达 日期
#     print(voys)
#     Prices = i['lowestPrices']  # 价格
#     for pri in Prices:
#         print(pri)