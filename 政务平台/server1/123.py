# coding=utf-8
# 作者    ： Administrator
# 文件    ：123.py
# IED    ：PyCharm
# 创建时间 ：2019/8/15 19:22

from PIL import Image
import pytesseract

# phone_img = Image.open('code/phone.png')
number_img = Image.open('code/number.png')
# 识别图片
# phone = pytesseract.image_to_string(phone_img)
number = pytesseract.image_to_string(number_img)
# print('成功获取手机号：{}'.format(phone))
print('成功获取身份证号：{}'.format(number))
