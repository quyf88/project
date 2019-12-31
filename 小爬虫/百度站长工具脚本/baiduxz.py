#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

files = {'file': ('img.jpg', open('img.jpg', 'rb'), 'image/jpeg', {})}


values = {'token': "5866ef7a9c779d6298dcdedc85c049a4"}
r = requests.post('http://106.13.108.81:882/api/Baiduyz', files=files, data=values)  # 成功
print(r)
print(r.text)
