import os
from PIL import Image, ImageDraw, ImageFont


def add_text(phone, name):
    """
    二维码图片添加文字
    :return:
    """
    # 加载字体文件
    ttfont = ImageFont.truetype("config/simhei.ttf", size=16)
    # 打开需要编辑的图片
    im = Image.open("config/流程图模板.png")
    width = im.size[0]
    # 创建一个可以在给定图像上绘图的对象(把图像改为可编辑模式)
    draw = ImageDraw.Draw(im)
    # 在给定的位置绘制一个字符串(在图像指定位置写入文字)
    # (x, y)位置, 文本, 字体颜色, 字体样式
    draw.text((170, 230), u'{}'.format(phone), fill=(0, 0, 0), font=ttfont)
    draw.text((215, 180), u'{}'.format(name), fill=(0, 0, 0), font=ttfont)
    # im.show()
    im.save(f'config/{name}.png')


def alipay_frame(name):
    """
    合成微信边框
    :return:
    """
    # 加载底图
    base_img = Image.open(r'config/微信收款模板.png')

    # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
    # print(base_img.size, base_img.mode)
    box = (280, 280, 800, 800)  # 底图上需要P掉的区域

    # 图片转换二维码 https://www.sojson.com/qr/image2qr.html
    input('图片转换二维码：https://www.sojson.com/qr/image2qr.html')

    # 加载需要P上去的二维码图片 图片转换后二维码
    tmp_img = Image.open(f'config/图片转换后二维码.png')
    # 这里可以选择一块区域或者整张图片
    # region = tmp_img.crop((0,0,304,546)) #选择一块区域
    # 或者使用整张图片
    region = tmp_img

    # 使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
    # 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
    # region = region.rotate(180) #对图片进行旋转
    # 将图片缩放至box区域大小
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    # 合成图片
    base_img.paste(region, box)
    # base_img.show() # 查看合成的图片
    base_img.save(f'image/{name}.png')  # 保存图片

    # 删除临时图片
    os.remove(f'config/{name}.png')


def run():
    phone = '18100000000'
    name = '测试'
    add_text(phone, name)
    alipay_frame(name)
    print('微信转账二维码生成成功')


if __name__ == '__main__':
    run()