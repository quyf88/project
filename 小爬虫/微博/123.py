# from configparser import ConfigParser
#
#
# def red_config():
#     """
#     读取配置文件
#     :return: 记录版本号
#     """
#     cp = ConfigParser()  # 实例化
#     cp.read('config/config.ini', encoding='utf-8')  # 读取文件
#     proxy = cp.get('Status', 'proxy')  # 读取值
#     return proxy
#
#
# if __name__ == '__main__':
#     proxy = red_config()
#     print(proxy)

import sys
from PyQt5.QtWidgets import QApplication, QWidget,QTextEdit
from PyQt5.QtGui import QTextCharFormat

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300,300)
        t = QTextEdit('我爱学习', self)   #创建多行文本对象
        #参数1  显示的文本
        #参数2  父控件
        #注意  光标在0位置
        t.setPlaceholderText('占位提示')   #在文本框内部内容为空时, 给用户的文本提示信息
        s=t.placeholderText()   #返回占位提示信息
        #
        # t.setPlainText('我爱我的祖国') #设置普通文本，原来的文本被覆盖掉

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())