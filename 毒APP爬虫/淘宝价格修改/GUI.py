# -*- coding: utf-8 -*-
# @Time    : 2019/6/4 8:51
# @Author  : project
# @File    : 测试测试.py
# @Software: PyCharm

import sys
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTextBrowser, QLineEdit

import res
from 毒APP爬虫.淘宝价格修改.SeleniumTomation import Spider


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(600, 400)
        self.setWindowTitle('淘宝在售商品价格修改')
        self.setWindowIcon(QIcon(':reson/maoyan.ico'))

        # 初始化搜索文本框
        self.movie_name = QLineEdit(self)
        # 初始化运行时间间隔文本框
        self.remove_name = QLineEdit(self)
        # 初始化启动按钮
        self.start_btn = QPushButton(self)

        # 初始化输出文本框
        self.log_browser = QTextBrowser(self)

        # 初始化水平布局
        self.h_layout = QHBoxLayout()
        # 初始化垂直布局
        self.v_layout = QVBoxLayout()

        # 初始化音频播放
        self.btn_sound = QSound(':reson/btn.wav', self)
        self.finish_sound = QSound(':reson/finish.wav', self)

        # 实例化线程
        self.worker = MyThread()

        # 实例化
        self.movie_init()
        self.start_btn_init()
        self.remove_init()
        self.layout_init()

    def movie_init(self):
        """增减价格输入框默认配置"""
        # 设置文本框尺寸
        self.movie_name.setFixedSize(150, 30)
        # 设置默认文本
        self.movie_name.setPlaceholderText("输入增减价格(元)")
        # 限制10个中文字符
        self.movie_name.setMaxLength(10)

    def remove_init(self):
        """运行时间间隔文本框默认配置"""
        # 设置文本框尺寸
        self.remove_name.setFixedSize(150, 30)
        # 设置默认文本
        self.remove_name.setPlaceholderText("输入程序运行间隔时间(默认3s)")
        # 限制10个中文字符
        self.remove_name.setMaxLength(10)

    def start_btn_init(self):
        """ 启动按钮按钮 配置"""
        self.start_btn.setText('启动')
        self.start_btn.setFixedSize(300, 30)
        self.start_btn.clicked.connect(self.start_btn_slot)

    def layout_init(self):
        """页面布局"""
        self.h_layout.addWidget(self.movie_name)
        self.h_layout.addWidget(self.remove_name)
        self.h_layout.addWidget(self.start_btn)

        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def start_btn_slot(self):
        """程序启动"""
        # 判断运行间隔时间
        if self.remove_name.text():
            remove_time = self.remove_name.text()
        else:
            remove_time = 3
        self.btn_sound.play()
        self.log_browser.append('<font color="red">程序启动</font>')
        self.log_browser.append('<font color="red">增减价：{}元,运行间隔：{}秒</font>'.format(self.movie_name.text(), remove_time))
        # 设置按钮状态
        self.start_btn.setEnabled(False)
        # 启动线程
        self.worker.price = self.movie_name.text()
        self.worker.remove_time = remove_time
        self.worker.start()
        self.finish_sound.play()
        self.start_btn.setEnabled(True)


class MyThread(QThread):
    trigger = pyqtSignal()
    remove_time = None
    price = None

    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        # 重写父类run 启动子进程
        tomation = Spider()
        tomation.main(self.price, self.remove_time)


def read_qss(style):
    file = QFile(style)
    file.open(QFile.ReadOnly)
    return QTextStream(file).readAll()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = CrawlWindow()
    qss_style = read_qss(':reson/style.qss')
    window.setStyleSheet(qss_style)
    window.show()
    sys.exit(app.exec_())

