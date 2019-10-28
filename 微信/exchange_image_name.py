# -*- coding:utf-8 -*-
# 文件 ：exchange_image_name.py
# IED ：PyCharm
# 时间 ：2019/10/28 0028 11:07
# 版本 ：V1.0
import os
import re
import time
import shutil
import pandas as pd


FILE_NAME = None  # 文件名
IMAGE_NAME = None  # 临时图片名列表


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
        MD5 = 0  # 校验码
        for i in range(len(df.keys())):
            if df.keys()[i] == '图片':
                image_name = i
            if df.keys()[i] == '校验码':
                MD5 = i
        # 循环每一行
        for indexs in df.index:
            # 读取指定行列数据 df.ix[行,列]
            image_num = df.ix[indexs, image_name]
            check_code = df.ix[indexs, MD5]
            # 修改指定单元格数据df.iloc[行, 列]
            if image_num == '无图片':
                continue

            # 图片数量 校验码
            yield image_num, check_code

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
            # 移动文件
        shutil.move(filename, f'ExportFile/image/{FILE_NAME}/')


def get_image_name():
    """
    读取图片文件名
    :return:
    """
    global IMAGE_NAME
    IMAGE_NAME = []
    # 提取图片数量
    for image_num, check_code in read_image_name():
        image_num = len(eval(image_num))

        global FILE_NAME
        files = os.listdir(f'ExportFile/image/{FILE_NAME}/')
        files = [i for i in files if 'jpg' in i]
        # print(files)
        for i in range(image_num):
            # print(files[i], check_code)
            save_image(files[i], check_code)
            IMAGE_NAME.append(files[i])


def save_image(image_name, check_code):
    """
    保存图片
    :return:
    """
    # 判断目录是否存在 没有则创建
    global FILE_NAME
    image_file = os.path.exists(f'ExportFile/image/{FILE_NAME}/{check_code}')
    if not image_file:
        os.makedirs(f'ExportFile/image/{FILE_NAME}/{check_code}')
        print('文件创建成功')
    # 移动图片至新目录
    old_directory = f'ExportFile/image/{FILE_NAME}/{image_name}'
    new_directory = f'ExportFile/image/{FILE_NAME}/{check_code}/{image_name}'
    shutil.move(old_directory, new_directory)


if __name__ == '__main__':
    get_image_name()
