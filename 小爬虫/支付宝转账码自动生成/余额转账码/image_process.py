import os
from PIL import Image, ImageDraw, ImageFont


class Picture:
    def __init__(self):
        self.text = 'qq_1033383881'

    def new_image(self):
        """
        创建空白图片
        :return:
        """
        # 合并二维码用
        img = Image.new('RGB', (120, 50), (255, 255, 255))
        img.save('image/1.png')
        # 合并支付宝边框用
        img1 = Image.new('RGB', (200, 75), (255, 255, 255))
        img1.save('image/2.png')

    def pinjie(self):
        """
        拼接图片
        :return:
        """
        # 获取当前文件夹中所有png图像
        Image.open('image/1.png')
        im_list = [fn for fn in os.listdir('image/') if '.png' in fn if 'splice.png' not in fn if '2.png' not in fn]
        im_list.reverse() if im_list[0] == '1.png' else im_list
        # print(im_list)
        im_list = [Image.open('image/' + fn) for fn in im_list]

        # 图片转化为相同的尺寸
        ims = []
        for i in im_list:
            new_img = i.resize((120, 120), Image.BILINEAR)
            ims.append(new_img)

        # 单幅图像尺寸
        width, height = ims[0].size
        # 创建空白长图 ims[0].mode格式 (width, height * len(ims)) 尺寸
        result = Image.new(ims[0].mode, (width, height * len(ims)))
        # 拼接图片
        for i, im in enumerate(ims):
            result.paste(im, box=(0, i * width))
        # 保存图片
        result.save('image/splice.png')

    def crop_img(self):
        """
        剪裁图片
        :return:
        """
        # 加载原始图片
        img = Image.open("image/splice.png")
        width = img.size[0]  # 图片大小
        height = img.size[1]
        # print(width, height)
        # img3 = img.crop((width - 120, height - 140, width, height))
        img3 = img.crop((0, 0, width, height - 105))
        img3.save('image/splice.png')

    def add_text(self):
        """
        二维码图片添加文字
        :return:
        """
        # 加载字体文件
        ttfont = ImageFont.truetype("config/simhei.ttf", size=12)
        # 打开需要编辑的图片
        im = Image.open("image/splice.png")
        width = im.size[0]
        # 创建一个可以在给定图像上绘图的对象(把图像改为可编辑模式)
        draw = ImageDraw.Draw(im)
        # 在给定的位置绘制一个字符串(在图像指定位置写入文字)
        # (35, 5)位置, 文本, 字体颜色, 字体样式
        draw.text((40, 120), u'{}'.format(self.text.replace(self.text[0], '*')), fill=(0, 0, 0), font=ttfont)
        # im.show()
        im.save('image/splice.png')

    def alipay_frame(self):
        """
        合成支付宝边框
        :return:
        """
        # 加载底图
        base_img = Image.open(r'config/支付宝模板.png')
        # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
        # print(base_img.size, base_img.mode)
        box = (150, 450, 740, 1135)  # 底图上需要P掉的区域

        # 加载需要P上去的图片
        tmp_img = Image.open(r'image/splice.png')
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
        base_img.save('image/splice.png')  # 保存图片

    def word_processing(self):
        """
        字体模糊处理
        :return:
        """
        # 打开底图
        img = Image.open("image/splice.png")
        box = (320, 1055, 520, 1130)  # 底图上需要P掉的区域

        # 加载需要P上去的图片
        img1 = Image.open("image/2.png")
        # 合成 底图区域必须和P上去的size一样大小
        img.paste(img1, box)

        # 添加文字
        # 加载字体文件
        ttfont = ImageFont.truetype("config/simhei.ttf", size=50)
        # 创建一个可以在给定图像上绘图的对象(把图像改为可编辑模式)
        draw = ImageDraw.Draw(img)
        # 在给定的位置绘制一个字符串(在图像指定位置写入文字)
        # (35, 5)位置, 文本, 字体颜色, 字体样式
        draw.text((355, 1065), u'{}'.format(self.text.replace(self.text[0], '*')), fill=(50, 50, 50), font=ttfont)

        # 保存图片
        image_name = 'image/code/' + self.text + '.png'
        img.save(image_name)

    def remove_temporary_image(self):
        """
        删除临时图片
        :return:
        """
        os.remove('image/1.png')
        os.remove('image/2.png')
        os.remove('image/code.png')
        os.remove('image/splice.png')

    def run(self):
        self.new_image()
        self.pinjie()
        self.crop_img()
        self.add_text()
        self.alipay_frame()
        self.word_processing()
        self.remove_temporary_image()


if __name__ == '__main__':
    spider = Picture()
    spider.run()
