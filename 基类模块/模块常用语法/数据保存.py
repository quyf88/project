# -*- coding:utf-8 -*-
# 文件 ：数据保存.py
# IED ：PyCharm
# 时间 ：2019/10/23 0023 12:21
# 版本 ：V1.0

def save_data(self, datas):
    """
    数据存储 json
    :return:
    """
    filename = 'PLC.json'
    for data in datas:
        with open(filename, 'a+') as f:
            # ensure_ascii 不适用ascii编码 解决不能显示中文问题
            json.dump(data, f, ensure_ascii=False)
            # 插入换行符
            f.write('\n')
            print(f'第：{self.count}条数据成功写入!')
            self.count += 1


def save_data(self, data):
    """保存为csv"""
    with open("twitter.csv", "a+", encoding='utf-8', newline="") as f:
        k = csv.writer(f, delimiter=',')
        with open("twitter.csv", "r", encoding='utf-8', newline="") as f1:
            reader = csv.reader(f1)
            if not [row for row in reader]:
                k.writerow(['ID', '推文数量', '关注人数', '关注列表', '粉丝数', '推文内容', '评论数', '转发数', '点赞数'])
                k.writerows(data)
            else:
                k.writerows(data)
        print(f'第：{self.count}条数据插入成功!')