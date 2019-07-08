# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 14:31
# @Author  : project
# @File    : 123.py
# @Software: PyCharm

#!/usr/bin/env python3
import asyncio

async def func_normal():
    print('A')
    await asyncio.sleep(1)
    print('B')
    return 'saad'

async def func_infinite():
    for i in range(10):
        print("--%d" % i)
    return 'saad2'

loop = asyncio.get_event_loop()
tasks = [func_normal(), func_infinite()]
results = loop.run_until_complete(asyncio.gather(*tasks))
print("func_normal()={}, func_infinite()={}".format(*results))
loop.close()
