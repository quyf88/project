# coding=utf-8
# 作者    ： Administrator
# 文件    ：get_comment.py
# IED    ：PyCharm
# 创建时间 ：2019/5/30 22:21


import re
import requests
from lxml import etree
from urllib.parse import quote
from fake_useragent import UserAgent


class GetComment:

    def __get_headers(self):
        return {"User-Agent": UserAgent().random}

    def new_url_list(self, word):
        """根据关键词获取视频地址列表"""
        url = 'https://search.bilibili.com/all?keyword={}'.format(quote(word, encoding='UTF-8'))
        response = requests.get(url, headers=self.__get_headers())
        content = response.content.decode(encoding='UTF-8')
        et_html = etree.HTML(content)
        new_url_list = et_html.xpath('//ul[@class="video-contain clearfix"]/li/a/@href')

        return new_url_list

    def comment_oid_list(self, word):
        """获取评论视频oid列表"""
        comment_url_list = self.new_url_list(word)
        comment_oids_list = [re.findall(r'av(.*)\?', i)for i in comment_url_list]
        comment_oid_list = [i for j in comment_oids_list for i in j]

        return comment_oid_list

    def comment_url_list(self, word):
        """拼接评论url"""

        comment_url_list = []
        comment_oid_list = self.comment_oid_list(word)
        numbers = [i for i in range(1, 5)]
        for comment_oid in comment_oid_list:
            for number in numbers:
                comment_url = 'https://api.bilibili.com/x/v2/reply?type=1&oid={0}&pn={1}'.format(comment_oid, number)
                comment_url_list.append(comment_url)

        return comment_url_list

    def comment_message(self, word):
        """获取评论"""

        comment_url_list = self.comment_url_list(word)

        for url in comment_url_list:
            try:
                comment_reaponse = requests.get(url, headers=self.__get_headers())
                comment_json = comment_reaponse.json()
                comment_content_list = comment_json['data']['replies']
                comment_message = [i['content']['message'] for i in comment_content_list]
                self.save_to_txt(comment_message)

                yield comment_message

            except Exception as e:
                print(e)
                continue

    def save_to_txt(self, comment):
        """保存为txt"""

        with open('reson/wordcloud.txt', 'a+', encoding='utf-8') as f:
            try:
                for i in comment:
                    f.write(i)
                    print("成功写入一条数据")
            except:
                print('保存完成')


if __name__ == '__main__':
    comment = GetComment()
    a = comment.comment_message('华为')
    print(next(a))



