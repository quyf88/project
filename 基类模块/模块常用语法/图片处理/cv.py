import cv2
import os

# 定义i进行计数，方便此后图片的命名
i = 0

# 输入、输出路径
indir = '' ''
outdir = '' ''

# 定义函数对单个图片进行处理并保存
# img -- 要处理的图片
# outdir -- 要保存的路径


def img_handle(img, outdir):
    global i
    cv2.imread(indir + '/' + img)
    # 在此进行图片的具体操作
    #
    #
    cv2.imwrite(outdir + '/' + 名字, new_img)
    i = i + 1

# 运用os获取指定文件夹的文件列表


imlist = os.listdir(indir)

for img in imlist:
    img_handle(img, outdir)