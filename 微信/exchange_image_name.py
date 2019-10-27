# coding=utf-8
# 作者    ： Administrator
# 文件    ：exchange_image_name.py
# IED    ：PyCharm
# 创建时间 ：2019/10/27 11:00
import os
import re
import time
import shutil
import pandas as pd

FILE_NAME = None
IMAGE_NAME = None


def read_image_name():
    """
    读取记录文件图片名
    :return:
    """
    count = 1
    files = os.listdir('.')
    filenames = [i for i in files if 'csv' in i if '备份' not in i]
    print(filenames)
    for filename in filenames:
        # 提取文件名
        (file_name, extension) = os.path.splitext(filename)
        global FILE_NAME
        FILE_NAME = file_name

        df_read = pd.read_csv(filename)
        df = pd.DataFrame(df_read)
        # 获取指定表头的列数
        image_name = 0  # 图片
        for i in range(len(df.keys())):
            if df.keys()[i] == '图片':
                image_name = i
        # 循环每一行
        for indexs in df.index:
            # 读取指定行列数据 df.ix[行,列]
            data1 = df.ix[indexs, image_name]
            # 修改指定单元格数据df.iloc[行, 列]
            if data1 == '无图片':
                continue

            yield data1
            # 修改文件名
            global IMAGE_NAME
            print(IMAGE_NAME)
            df.iloc[indexs, image_name] = ','.join(IMAGE_NAME)
            # 查询一条保存一条
            df.to_csv(filename, index=False, encoding='utf_8_sig')
            print(f'成功修改：{count}条数据')
            # 备份
            shutil.copy(filename, '备份数据.csv')
            count += 1
            # 清空记录列表
            IMAGE_NAME = []


def get_record_time():
    """
    记录文件时间戳转换日期
    :return:
    """
    for image_names in read_image_name():
        # eval 剔除字符串 前后标点
        # image_names = eval(image_names)
        image_names = re.findall(r'mmexport(.*?).jpg', image_names)
        for image_name in image_names:
            timeStamp = int(image_name) / 1000
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

            yield otherStyleTime


def get_image_name():
    """
    读取图片文件名
    :return:
    """
    global IMAGE_NAME
    IMAGE_NAME = []
    for i in get_record_time():
        files = os.listdir(f'ExportFile/image/{FILE_NAME}/')
        # print(files)
        for image_name in files:
            image_name_time = re.findall(r'mmexport(.*?).jpg', image_name)[0]
            timeStamp = int(image_name_time) / 1000
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            if i == otherStyleTime:
                IMAGE_NAME.append(image_name)
                break



if __name__ == '__main__':
    get_image_name()
