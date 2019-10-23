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