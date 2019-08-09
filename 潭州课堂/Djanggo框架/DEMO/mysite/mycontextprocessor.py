# -*- coding: utf-8 -*-
# @Time    : 2019/8/9 11:17
# @Author  : project
# @File    : mycontextprocessor.py
# @Software: PyCharm


def my_user(request):
    """
    上下文管理器
    需要在主项目文件setting TEMPLATES 中配置
    """
    username = request.session.get('username', '不存在')
    return {'myuser': username}