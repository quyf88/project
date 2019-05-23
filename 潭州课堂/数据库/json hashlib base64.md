#### **JSON 数据操作**

```python
import json
"""
indent :格式化输出
ensure_ascii:是否用ascii码解析 默认True
"""
# dumps: python--->json
my_dict = {'name':'蛋蛋', 'age':2}
res = json.dumps(my_dict, indent=2，ensure_ascii=False)

#loads: json--->python
json.loads(res)

# dump: python--->json, 保存到文件中
my_dict = {'name':'蛋蛋', 'age':2}
with open('json_test', 'w+') as f:
    json.dump(my_dict, ensure_ascii=False, fp=f)
    
# load: json--->python, 从json文件中读取
with open('json_test', 'r+') as f:
    print(json.load(fp=f))    
```

#### **hashlib 加密（哈希算法）**

```python
import hashlib
"""
encode(): 编码  必须二进制
hexdigest:16进制
"""
# MD5
res = hashlib.md5('蛋蛋'.encode())
print(res.hexdigest()) # 获得str类型的结果
print(res.digest())  # 获得bytes类型的结果

# sha256
res = hashlib.sha256() # 创建对象 可多次调用
res.update('蛋蛋'.encode())
```

#### **base64 加密**

```python
import base64
"""
base64.b64encode()  对二进制数据进行base64编码
base64.b64decode()  对通过base64编码的数据进行解码
base64.urlsafe_b64encode()  对url进行base64编码
base64.urlsafe_b64decode()  对通过base64编码的url进行解码

"""

# 加密
data = '蛋蛋'
res = base64.b64enconde(data.encode())
# 解密
base64.b64decode(res.decode())
```

