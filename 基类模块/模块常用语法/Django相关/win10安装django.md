## **win10安装django 并 创建项目**

- ### **建立虚拟环境**
  安装virtualenv：pip install virtualenv

- ### **创建虚拟环境下的项目目录**
  virtualenv 项目文件夹名字

- ### **激活 **
  进入到new-env目录下进入到scripts文件夹下，windows下dir可以查看有什么文件，运行activate
  要停止使用虚拟环境，执行命令deactivate

- ### **安装django**
  pip install django

- ### **在django中创建项目**
  在Scripts文件夹下
  django-admin startproject 项目文件夹名字

- ### **创建数据库**
  进入到manage.py所在文件夹下，输入命令
  python manage.py migrate
  新增了一个db.sqlite3文件

- ### **查看项目**
  python manage.py runserver 8001
  打开网站查看是否正确，8001是端口号，可以自己设，重复的话换一个就好了。