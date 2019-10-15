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
    "Cookie": "install_id=53112482656; ttreq=1$a4ed279b42b9acb3dee9a3a3c2d645ce99ed786f; odin_tt=38d535495242f853ffdf693ae531a152910b1047bbb3ba5c8e2fa7f3cbd7f6a1ec9f6027fc44ea36c4bd45281487d4a7; sid_guard=d074b1c430eef87a3599e20ef34a5555%7C1543976393%7C5184000%7CSun%2C+03-Feb-2019+02%3A19%3A53+GMT; uid_tt=4e0b25bc326fae6b428afc5826243eeb; sid_tt=d074b1c430eef87a3599e20ef34a5555; sessionid=d074b1c430eef87a3599e20ef34a5555",
    "Accept-Encoding": "gzip",
    "X-SS-REQ-TICKET": "1543976807598",
    "X-Tt-Token": "00d074b1c430eef87a3599e20ef34a5555b97ecb95bff1a3d1a81726386a1adf7a91df6c32bfa121fc10400ffede8df72016",
    "sdk-version": "1",
    "X-SS-TC": "0",
    "User-Agent": "com.ss.android.ugc.aweme/350 (Linux; U; Android 8.0.0; zh_CN; MI 5; Build/OPR1.170623.032; Cronet/58.0.2991.0)"
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
        url = 'https://aweme-hl.snssdk.com/aweme/v1/discover/search/?cursor=' + str(cursor) + '&keyword=' + keys + '&offset=0&count=10&type=1&is_pull_refresh=0&hot_search=0&latitude=30.725991&longitude=103.968091&ts=1543984658&js_sdk_version=1.2.2&app_type=normal&manifest_version_code=350&_rticket=1543984657736&ac=wifi&device_id=60155513971&iid=53112482656&os_version=8.0.0&channel=xiaomi&version_code=350&device_type=MI%205&language=zh&uuid=862258031596696&resolution=1080*1920&openudid=8aa8e21fca47053b&update_version_code=3502&app_name=aweme&version_name=3.5.0&os_api=26&device_brand=Xiaomi&ssmix=a&device_platform=android&dpi=480&aid=1128&as=a1e5055072614ce6a74033&cp=5813c65d2e7d0769e1[eIi&mas=01327dcd31044d72007555ed00c3de0b5dcccc0c2cec866ca6c62c'
        # 获取搜索界面并转化为json对象
        print(url)
        jsonObj = json.loads(post_html(url))
        print(post_html(url))
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