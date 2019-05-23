# coding=utf-8
# 作者    ： Administrator
# 文件    ：my_redis.py
# IED    ：PyCharm
# 创建时间 ：2019/5/19 16:14
"""
# 1.建立连接
#conn = redis.StrictRedis(db=0, decode_responses=True)
# 2.使用redis命令

# 增
rpush list_a hello world python # 自右向左增加
lpush list_a 1 2 3 # 自左向右增加
# 删
rpop list_a # 删除末尾一个元素
lpop list_a # 删除开头一个元素
lrem list_a 0 hello # 删除指定下标和值 成功返回1 失败返回0
# 改
lset list_a 0 haha # 指定下标 和值
# 查
lrange list_a 0 10 # 指定查询开始和结束索引
lindex list_a 2 # 指定下标查询

# 增
res = conn.rpush('hello', 'world', 'python')
print(res)
res = conn.lpush('hello', '123')
print(res)
# 查
rang = conn.lrange('hello', 0, 10)  # 索引查询
print(rang)
index = conn.lindex('hello', 0)  # 下标查询
print(index)
# 改
l_set = conn.lset('hello', 0, 'ha')
print(l_set)
# 删
rem = conn.rpop('hello')
print(rem)
rem = conn.lpop('hello')
print(rem)
# rem = conn.lrem('hello', 0)
"""
import redis


class Redis:
    def __init__(self, db=0, decode_responses=True):
        self.conn = redis.StrictRedis(db=db, decode_responses=decode_responses)

    def push(self, kay, *values, right=True):
        if right:
            result = self.conn.rpush(kay, *values)
        else:
            result = self.conn.lpush(kay, *values)
        return result

    def remove(self, key, value=None, right=True, sub=None):
        if value or sub:
            result = self.conn.lrem(key, sub, value)
        elif right is True:
            result = self.conn.rpop(key)
        else:
            result = self.conn.lpop(key)
        return result

    def search(self, key, start, end=None):
        if end:
            result = self.conn.lindex(key, start, end)
        else:
            result = self.conn.lrange(key, start)
        return result

    def update(self, key, value, index):
        result = self.conn.lset(key, index, value)
        return result
