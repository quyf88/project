import cv2
import os
import datetime


def change_size(read_file):
    image = cv2.imread(read_file, 1)  # 读取图片 image_name应该是变量
    img = cv2.medianBlur(image, 5)  # 中值滤波，去除黑色边际中可能含有的噪声干扰
    b = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)  # 调整裁剪效果
    binary_image = b[1]  # 二值图--具有三通道
    binary_image = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)
    print(binary_image.shape)  # 改为单通道

    x = binary_image.shape[0]
    print("高度x=", x)
    y = binary_image.shape[1]
    print("宽度y=", y)
    edges_x = []
    edges_y = []
    for i in range(x):
        for j in range(y):
            if binary_image[i][j] == 255:
                edges_x.append(i)
                edges_y.append(j)

    left = min(edges_x)  # 左边界
    right = max(edges_x)  # 右边界
    width = right - left  # 宽度
    bottom = min(edges_y)  # 底部
    top = max(edges_y)  # 顶部
    height = top - bottom  # 高度

    pre1_picture = image[left:left + width, bottom:bottom + height]  # 图片截取
    return pre1_picture  # 返回图片数据


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print("程序开始时间：{}".format(start_time))
    source_path = "."  # 图片来源路径    

    file_names = os.listdir(source_path)
    print(f'读取图片：{len(file_names)}张')
    starttime = datetime.datetime.now()
    for i in range(len(file_names)):
        print(f'第:{i+1}张图片处理中')        
        print(file_names[i])
        if 'png' not in file_names[i]:
            continue
        read_file = file_names[i]
        # 处理图片
        x = change_size(read_file)  # 得到文件名
        # 保存图片
        cv2.imwrite(read_file, x)
        print(f'第:{i+1}张处理完成')

    print("裁剪完毕")
    end_time = datetime.datetime.now()
    print("程序结束时间：{}".format(end_time))
    print("程序执行用时：{}s".format((end_time - start_time)))
