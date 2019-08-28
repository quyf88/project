from PIL import Image

# 读取图片
img = Image.open('1566963714847298068.png')
# 获取图片尺寸
(width, height) = img.size
print(width, height)
# 剪裁图片
phone_image = img.crop((0, 40, width, int(height)-55))
# 保存
phone_image.save('1.png')