# -*- coding: utf-8 -*-
# @Time    : 2019/7/22 15:48
# @Author  : project
# @File    : test.py
# @Software: PyCharm


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


def getHTML(url):
    '''
    get方式获取html
    :param url:
    :return:
    '''
    rsp = requests.get(url, headers=headers, verify=False)
    return rsp.content.decode(rsp.apparent_encoding, 'ignore')


def postHTML(url):
    '''
    post方式获取html
    :param url:
    :return:
    '''
    rsp = requests.post(url, headers=headers, verify=False)
    print(rsp.content.decode(rsp.apparent_encoding, 'ignore'))
    return rsp.content.decode(rsp.apparent_encoding, 'ignore')


def getVideo(key):
    '''
    获取第一个视频连接地址
    :param key:
    :return:
    '''
    # 编译关键词
    key = urllib.parse.quote(key)
    # 拼接关键词搜索接口url
    # hot_search 0普通搜索 1热门搜索
    # url = 'https://api.amemv.com/aweme/v1/general/search/single/?keyword=' + key + '&offset=0&count=10&is_pull_refresh=0&hot_search=0&latitude=30.725991&longitude=103.968091&ts=1543984658&js_sdk_version=1.2.2&app_type=normal&manifest_version_code=350&_rticket=1543984657736&ac=wifi&device_id=60155513971&iid=53112482656&os_version=8.0.0&channel=xiaomi&version_code=350&device_type=MI%205&language=zh&uuid=862258031596696&resolution=1080*1920&openudid=8aa8e21fca47053b&update_version_code=3502&app_name=aweme&version_name=3.5.0&os_api=26&device_brand=Xiaomi&ssmix=a&device_platform=android&dpi=480&aid=1128&as=a1e5055072614ce6a74033&cp=5813c65d2e7d0769e1[eIi&mas=01327dcd31044d72007555ed00c3de0b5dcccc0c2cec866ca6c62c'
    url = 'https://aweme-hl.snssdk.com/aweme/v1/discover/search/?cursor=0&keyword=' + key +'&count=10&type=1&is_pull_refresh=1&hot_search=0&ts=1563785163&js_sdk_version=1.13.10&app_type=normal&os_api=25&device_platform=android&device_type=OS105&iid=72586330332&ssmix=a&manifest_version_code=590&dpi=400&uuid=86795503044051&version_code=590&app_name=aweme&version_name=5.9.0&openudid=c2f22121e41a5d07&device_id=50751127063&resolution=1080*2070&os_version=7.1.1&language=zh&device_brand=SMARTISAN&ac=wifi&update_version_code=5902&aid=1128&channel=smartisan&_rticket=1563785162163&mcc_mnc=46000&as=a125c7e3ab0ced87754277&cp=79cedb5eb4553a7ee1OaWe&mas=011c8e49f4af7b5cbff404b102685f2d16ecec4c2cacecec1c26a6'
    print(url)
    # 获取搜索界面并转化为json对象
    jsonObj = json.loads(postHTML(url))
    # 获取data对应v
    metes = jsonObj['data']
    nums = len(metes)
    uri = ''
    # 多个视频列表捕获第一个视频地址即刻返回视频uri(视频唯一标识)
    for _ in range(nums):
        data = metes[_]['aweme_info']['video']
        if 'download_suffix_logo_addr' in data.keys():
            uri = data['download_suffix_logo_addr']['uri']
            break
    # 拼接视频地址
    videoURL = 'https://aweme.snssdk.com/aweme/v1/playwm/?video_id=' + uri + '&line=0'
    # 返回视频地址
    return videoURL


def main():
    '''
    入口函数
    :return:
    '''
    ts = str(time.time())
    # 入口url（热门列表url）
    # url = 'https://aweme.snssdk.com/aweme/v1/hot/search/list/?detail_list=0&ts=' + ts + '&js_sdk_version=1.2.2&app_type=normal&manifest_version_code=350&_rticket=1543976807872&ac=wifi&device_id=60155513971&iid=53112482656&os_version=8.0.0&channel=xiaomi&version_code=350&device_type=MI%205&language=zh&resolution=1080*1920&openudid=8aa8e21fca47053b&update_version_code=3502&app_name=aweme&version_name=3.5.0&os_api=26&device_brand=Xiaomi&ssmix=a&device_platform=android&dpi=480&aid=1128&as=a1c56320b7f6ccc7874900&cp=3d63c15f7576037de1_uMy&mas=01258b5acd59f6bccb58178086286fdded0c0c9c2cec1cecc6c6c6'
    url = 'https://aweme-hl.snssdk.com/aweme/v1/hot/search/list/?detail_list=1&ts=' + ts + '&js_sdk_version=1.13.10&app_type=normal&os_api=25&device_platform=android&device_type=OS105&iid=72586330332&ssmix=a&manifest_version_code=590&dpi=400&uuid=86795503044051&version_code=590&app_name=aweme&version_name=5.9.0&openudid=c2f22121e41a5d07&device_id=50751127063&resolution=1080*2070&os_version=7.1.1&language=zh&device_brand=SMARTISAN&ac=wifi&update_version_code=5902&aid=1128&channel=smartisan&_rticket=1563784042750&mcc_mnc=46000&as=a1a56733bb86ed03654600&cp=746bd557b3573c37e1QaYe&mas=01b602080bf461332c19a32bfd3e4bc9b80c0c6c2cac6ccc0c26a6'
    # 获取热门列表数据
    html = getHTML(url)
    # 转化为json对象
    jsonObj = json.loads(html)
    # 获取每一个热门数据列表
    word_list = jsonObj['data']['word_list']
    index = 1
    # 循环解析每个热门事件
    for li in word_list:
        try:
            # 关键词
            word = li['word']
            # 热度值
            hot_value = li['hot_value']
            # 排名
            hot_index = index
            # videoURL = getVideo(word)
            # 拼接视频下载地址
            videoURL = getVideo('吃鸡搞笑视频')
            index += 1
            print("排名：%d ,关键词: %s ,热度值: %d ,视频下载地址: %s" % (hot_index, word, hot_value, videoURL))
        except Exception as e:
            pass
        finally:
            time.sleep(3)


if __name__ == '__main__':
    # main()
    getVideo('吃鸡搞笑视频')
