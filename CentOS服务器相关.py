# -*- coding:utf-8 -*-
# 文件 ：CentOS服务器相关.py
# IED ：PyCharm
# 时间 ：2020/3/26 0026 0:27
# 版本 ：V1.0

"""nohup 后台不间断运行程序"""
# 2>&1:错误和输出都传到nohup.out文件中;&:后台运行
# nohup python spider.py 2>&1 &
# >./log.txt:错误和输出都传到log.txt文件中
# nohup python spider.py >./log.txt  2>&1 &
# ps -ef | grep python  查看python进程


"""进程操作"""
# 根据程序名杀死进程
# ps -ef | grep 程序名 | grep -v grep | awk '{print $2}' | xargs kill -9

# 启动服务
# service uwsgi start

# nginx热加载
# nginx -s reload