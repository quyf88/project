# coding=utf-8
# 作者    ： Administrator
# 文件    ：123.py
# IED    ：PyCharm
# 创建时间 ：2019/8/11 19:28
from PIL import Image
import tesserocr
import sys
import fateadm_api
# im = Image.open('./code/phone_page.png')
# im = im.crop((310, 160, 500, 185))
# im.save('./code/phone.png')
# print('成功获取手机号图片')
# img = Image.open('code/phone.png')
# phone = tesserocr.image_to_text(img)
# print(phone)


def spot_code(balances=False):
    """
    验证码识别
    balances 查询余额
    :return:
    """
    # 斐斐打码
    print('---验证码识别中---')
    count = 1
    while True:
        if balances:
            balance = fateadm_api.TestFunc(balances=True)
            if balance < 1000:
                print('余额不足及时充值：{}'.format(balance))
            elif balance < 100:
                print('余额严重不足即将不能使用：{}'.format(balance))
            elif balance < 10:
                print('*' * 30)
                print('余额不足,请充值：{}'.format(balance))
                print('*' * 30)
                sys.exit()
            return print('打码平台余额：{}'.format(balance))
        rsp = fateadm_api.TestFunc()
        if count > 3:
            print('验证码识别失败! 请联系开发者')
            sys.exit()
        if not rsp.pred_rsp.value:
            count += 1
            continue
        return rsp.pred_rsp.value


code = spot_code()

print(code)