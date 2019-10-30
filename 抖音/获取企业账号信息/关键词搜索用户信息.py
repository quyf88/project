# -*- coding: utf-8 -*-
# @Time    : 2019/7/23 14:44
# @Author  : project
# @File    : 关键词搜索用户信息.py
# @Software: PyCharm
import csv
import requests
import json
import urllib.parse
import time

headers = {
    "Cookie": "odin_tt=a8bed7a56345dbebad260171984832799b98f126343f4a11be86609b413a432335420b9b056856f23c2e5631938a23478aea2faefe63fe951e622107974b7dd9; install_id=90643239490; ttreq=1$691cae420b20487b834adc19d976b60b5ed6541d",
    "Accept-Encoding": "gzip",
    "X-Gorgon": "03006cc00604d4456509fdb41d0fe0c14e794f5048c7e5b548d1",
    "X-Khronos": "1572416727",
    "X-SS-REQ-TICKET": "1572416727320",
    "X-SS-STUB": "5D9F737C00F3EB033FD4277DC45B6E92",
    "x-tt-trace-id": "00-6b63a1cbf7fc7098b268390b3daf455b-6b63a1cbf7fc7098-01",
    "sdk-version": "1",
    "X-SS-TC": "0",
    "User-Agent": "com.ss.android.ugc.aweme/840 (Linux; U; Android 7.1.1; zh_CN; OS105; Build/NGI77B; Cronet/58.0.2991.0)"
}
count = 0


def post_html(url):
    """
    post方式获取html
    :param url:
    :return:
    """
    rsp = requests.post(url, headers=headers, verify=False)
    # return rsp.content.decode(rsp.apparent_encoding, 'ignore')
    return rsp.content.decode(encoding='utf-8')


def get_video(key):
    """
    根据关键词搜索用户信息
    :param key:
    :return:
    """
    # 编译关键词
    keys = urllib.parse.quote(key)
    # 下一页
    cursor = 0
    while True:
        # 拼接用户搜索接口url
        # hot_search 0普通搜索 1热门搜索 type=1 用户列表
        url = 'https://aweme-hl.snssdk.com/aweme/v1/discover/search/?cursor=' + str(cursor) + '&keyword=' + keys + '&offset=0&count=10&type=1&is_pull_refresh=0&hot_search=1&latitude=30.725991&longitude=103.968091&ts=1543984658&js_sdk_version=1.2.2&app_type=normal&manifest_version_code=350&_rticket=1543984657736&ac=wifi&device_id=60155513971&iid=53112482656&os_version=8.0.0&channel=xiaomi&version_code=350&device_type=MI%205&language=zh&uuid=862258031596696&resolution=1080*1920&openudid=8aa8e21fca47053b&update_version_code=3502&app_name=aweme&version_name=3.5.0&os_api=26&device_brand=Xiaomi&ssmix=a&device_platform=android&dpi=480&aid=1128&as=a1e5055072614ce6a74033&cp=5813c65d2e7d0769e1[eIi&mas=01327dcd31044d72007555ed00c3de0b5dcccc0c2cec866ca6c62c'
        # url = 'https://aweme-hl.snssdk.com/aweme/v1/discover/search/?cursor=0&keyword=%E6%8E%A8%E5%B9%BF&count=10&type=1&is_pull_refresh=0&hot_search=0&search_source=&search_id=&query_correct_type=1&os_api=25&device_type=OS105&ssmix=a&manifest_version_code=840&dpi=400&uuid=86795503044051&app_name=aweme&version_name=8.4.0&ts=1572416728&app_type=normal&ac=wifi&channel=smartisan&update_version_code=8402&_rticket=1572416727321&device_platform=android&iid=90643239490&version_code=840&openudid=c2f22121e41a5d07&device_id=50751127063&resolution=1080*2070&device_brand=SMARTISAN&language=zh&os_version=7.1.1&aid=1128&mcc_mnc=46001'
        # 获取搜索界面并转化为json对象
        print(url)
        jsonObj = json.loads(post_html(url))
        print(post_html(url))

        import os
        os._exit(0)

        metes = jsonObj['user_list']

        nums = len(metes)
        for _ in range(nums):
            # 抖音号
            short_id = metes[_]['user_info']['short_id']
            # UID
            uid = metes[_]['user_info']['uid']
            # 昵称
            nickname = metes[_]['user_info']['nickname']
            # 个性签名
            signature = metes[_]['user_info']['signature']
            signature = signature.replace('\n', '  ')
            # 性别 1=男 2=女 0=未知
            gender = metes[_]['user_info']['gender']
            gender = '男' if gender == 1 else '女' if gender == 2 else '未知'
            # 年龄
            birthday = metes[_]['user_info']['birthday']
            if birthday:
                birthday = birthday.split('-')[0]
                now_year = time.strftime("%Y", time.localtime())
                birthday = int(now_year) - int(birthday)
            # 粉丝
            follower = metes[_]['user_info']['follower_count']
            # 关注
            following = metes[_]['user_info']['following_count']
            # 赞
            total_favorited = metes[_]['user_info']['total_favorited']
            # 个人主页
            user_url = 'https://www.douyin.com/share/user/{}'.format(uid)
            # 读取时间
            writertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data = ([[key, short_id, nickname, signature, gender, birthday, follower, following, total_favorited, user_url, writertime]])
            model_csv(data)
        # 没有下一页数据退出
        if not jsonObj['has_more']:
            break
        cursor += 10
        time.sleep(3)


def model_csv(data):
    """保存数据"""

    global count
    count += 1
    with open("demo.csv", "a+", encoding='utf-8', newline="") as f:
        k = csv.writer(f, delimiter=',')
        with open("demo.csv", "r", encoding='utf-8', newline="") as f1:
            reader = csv.reader(f1)
            if not [row for row in reader]:
                k.writerow(['关键词', '抖音号', '昵称', '个性签名', '性别', '年龄', '粉丝', '关注', '赞', '个人主页', '写入时间'])
                k.writerows(data)
                print('第[{}]条数据插入成功'.format(count))
            else:
                k.writerows(data)
                print('第[{}]条数据插入成功'.format(count))


if __name__ == '__main__':
    key = input('请输入关键词：')
    get_video(key)