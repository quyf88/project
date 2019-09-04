import os
from PIL import Image, ImageDraw, ImageFont


class Picture:
    def __init__(self):
        self.text = '陈小丽'

    def new_image(self):
        """
        创建一个空白图片
        :return:
        """
        img = Image.new('RGB', (120, 50), (255, 255, 255))
        img.save('image/1.png')

    def pinjie(self):
        """
        拼接图片
        :return:
        """
        # 获取当前文件夹中所有JPG图像
        Image.open('image/1.png')
        im_list = [fn for fn in os.listdir('image/') if '.png' in fn if 'splice.png' not in fn]
        im_list.reverse() if im_list[0] != '1.png' else im_list
        print(im_list)
        im_list = [Image.open('image/' + fn) for fn in im_list]

        # 图片转化为相同的尺寸
        ims = []
        for i in im_list:
            new_img = i.resize((120, 120), Image.BILINEAR)
            ims.append(new_img)

        # 单幅图像尺寸
        width, height = ims[0].size
        # 创建空白长图
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
        img3 = img.crop((width - 120, height - 140, width, height))
        img3.save('image/splice.png')

    def add_text(self):
        """
        图片添加文字
        :return:
        """
        ttfont = ImageFont.truetype("image/simhei.ttf", 15)
        im = Image.open("image/splice.png")
        draw = ImageDraw.Draw(im)
        draw.text((35, 5), u'{}'.format(self.text), fill=(0, 0, 0), font=ttfont)
        # im.show()
        image_name = 'image/code/' + self.text + '.png'
        im.save(image_name)

    def run(self):
        self.new_image()
        self.pinjie()
        self.crop_img()
        self.add_text()
        os.remove('image/splice.png')


if __name__ == '__main__':
    spider = Picture()
    spider.run()
