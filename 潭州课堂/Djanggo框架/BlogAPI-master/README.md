# 基于Django的开源博客项目

> 大家好,我是抖音号lxgzhw的作者,目前为止,Django博客
> 已经做了几十遍了,决定写一个开源项目,供入门者学习.

## 1.1 模型
> 模型在api.models中,有详细注释
> 为了方便大家,我用的sqlite3数据库
> 只要大家环境配好,能够直接使用,免去了
> 很多的麻烦

## 1.2 基本功能
-  文章列表页的搜索功能
-  文章列表页的分类导航功能
-  点击文章进入详情页的功能
-  分页功能
-  首页搜索功能

## 1.3 环境依赖说明
> 依赖环境在requirements.txt里面

## 1.4 安装环境命令
```
pip install -r requirements.txt
```
## 1.5 启动项目命令
```
python manage.py runserver
```

## 1.6 后台登录
```
用户名: lxg
密码: lxgzhw00
地址: http://127.0.0.1:8000/admin
```

## 2.1 更新说明
- 增加点赞功能
- 增加点踩功能
- 增加错误提示功能
> 代码位于detail.html文件+Views文件detail函数中