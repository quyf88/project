#### **datatime 模块**

```python
from datetime import datetime
"""
时间日期对象.timestamp()：  时间日期转换为时间戳
datetime.fromtimestamp(时间戳)：时间戳转换为时间日期
时间日期对象.strftime(日期格式)： 时间日期转换为字符串
datetime.strptime(时间字符串，格式) ：字符串转换为时间日期
"""
# 日期时间和时间戳相互转换
now = datetime.now() # 获取当前系统时间
res = now.timestamp() # 日期转换为时间戳
res1 = datetime.fromtimestamp(res) # 时间戳转换为日期时间

# 日期格式化输出 %Y/%y年 %m月 %d日 %H/%l数 %M分 %S秒
res1.strftune('%Y年 %m月 %d日') # 时间日期转字符串
s = '11 1 2019 15:12:12'
datetime.strptime(s, '%d %m %Y %H:%M:%S')

# timedelta 时间计算
import datetime
now = datetime.datetime.now()
res = datetime.timedelta(houre=8,minutes=11,seconds=39)
now - res

```

#### **Logging 模块**

```python
import logging
"""
debug--->最低级别
info---->
warning-->
error--->
critical-->最高
"""
logging.basicConfig(
    level=logging.INFO, # 配置日志登记
    format='时间：%(asctime)s 文件名：%(filename)s 行号%(lineno)d', # 配置输入格式
    filename='my.log', # 配置写入文件名
    filemode='a', # 配置写入方式
)

# 模块化组件
"""

"""
# 1. 创建一个日志处理器
my_logger = logging.Logger('a') # 创建一个日志处理对象 可添加多个处理器

# 第一个处理器
mh = logging.FileHandler('test.log') # 定义一个handler
mh.setLevel(logging.INFO) # 配置日志级别
mft = logging.Formatter('时间：%(asctime)s 文件名：%(filename)s 行号%(lineno)d') # 定义日志格式器
mh.setFormatter(fmt) # 添加
my_logger.addHanler(mh)

# 第二个处理器
yh = logging.StreamHandler()
fmt1 = logging.Formatter('时间：%(asctime)s 文件名：%(filename)s 行号%(lineno)d')
yh.setFormatter(fmt1)
my_logger.addHadnler(yh)

# 使用
my_logger.info('我是日志组件')
```

