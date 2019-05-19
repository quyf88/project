#### **redis进入和退出**

```redis
redis-cli # 进入数据库 默认进入[0]
select 1 # 进入第二个数据库 共15个
exit # 退出
```

#### **全局key**

```
keys * # 查看全部
del key # 删除 del key名
rename key new_key # 修改key名
expire key ms # 设置过期时间
ttl key # 查看过期时间
persist key # 删除过期时间
```

#### **seting**

```
# 增
set a 1 # set key value
# 删
del a # del key
# 改
append a 2 # a=12 现有基础上增加
set a 2 # a=2 set key value 有则改无则增
# 查
get a # get key
```

#### **lsit**

```
# 增
rpush list_a hello world python # 自右向左增加
lpush list_a 1 2 3 # 自左向右增加
# 删
rpop list_a # 删除末尾一个元素
lpop list_a # 删除开头一个元素
lrem list_a 0 hello # 删除指定下标 成功返回1 失败返回0
# 改
lset list_a 0 haha # 指定下标 和值
# 查
lrange list_a 0 10 # 指定查询开始和结束索引
lindex list_a 2 # 指定下标查询
```

#### **hash**

```
# 增
hset hash_a a 1 # 增加一条
hmset hash_a b 2 c 3 # 增加多条
# 删
hdel hash_a a 
# 改
hset hash_a a 123 # 有则改无则增
# 查
hget hash_a a # 查询指定数据
hvals hash_a  # 查询所有值
hkeys hash_a  # 查询所有field
hgetall hash_a # 查询所有
```

#### set

```
# 增
sadd set_a hello world "hello world" # 增加多条
# 删
spop set_a # 随机删除一个
srem set_a hello world # 指定删除多个
# 查
smembers set_a # 查询所有
```

#### **zset**

```
# 增
zadd zset_a 1 hello 2 world 3 python # 增加多条
# 删
zrem zset_a hello # 删除指定值 可删除多个 空格 隔开
zremrangeburank zset_a 0 1 # 索引删除
zremrangebuscore zset_a 1 2 # 权重值删除
# 查
zrange zset_a 0 10 # 通过指定索引查询
zrangebyscore zset_a 1 2 # 通过权重查询
zadd zset_a 1 hello # 查看指定值权重
```





```python
import redis

# 1.建立连接
conn = redis.StrictRedis(db=0, decode_responses=True)
# 2.使用redis命令
"""(1)string"""
conn.set('k', 'v')
res = conn.get('k')
print(res)
"""(2)key操作"""
# 查看全部key
res = conn.keys('*')
print(res)
# 修改key名 返回true修改成功
res = conn.rename('k', 'key')
print(res)
# 删除 1 成功 0 失败
res = conn.delete('k')
print(res)
```







