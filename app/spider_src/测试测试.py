# -*- coding: utf-8 -*-
# @Time    : 2019/6/4 8:51
# @Author  : project
# @File    : 测试测试.py
# @Software: PyCharm
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream, QProcess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QTextBrowser, QTableWidget, \
    QTableWidgetItem, QHeaderView, QProgressBar, QHBoxLayout, QVBoxLayout, QMessageBox, QLineEdit

from app.spider_src.GUI import res
from app.spider_src import main
from app.spider_src import config


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle('毒APP数据采集')
        self.setWindowIcon(QIcon(':res/logo.ico'))

        # 初始化获取所有数据按钮
        self.start_btn = QPushButton(self)
        # 初始化获取xlsx按钮
        self.xlsx_btn = QPushButton(self)
        # 初始化输出文本框
        self.log_browser = QTextBrowser(self)
        # 初始化进度条
        self.progressbar = QProgressBar(self)

        # 初始化水平布局
        self.h_layout = QHBoxLayout()
        # 初始化垂直布局
        self.v_layout = QVBoxLayout()

        # 实例化启动程序
        # self.process = QProcess()
        self.threads = None
        self.config = config
        self.main = main

        # 初始化音频播放
        self.btn_sound = QSound(':res/btn.wav', self)
        self.finish_sound = QSound(':res/finish.wav', self)

        # 实例化
        self.start_btn_init()
        self.xlsx_btn_init()
        self.log_browser_init()
        self.progressbar_init()
        self.layout_init()
        # self.crawl_init()
        # self.process_init()

    # def process_init(self):
    #
    #     self.process.readyReadStandardOutput.connect(self.addStdOut)
    #     self.process.readyReadStandardError.connect(self.addStdOut)
    #     # self.process.finished.connect(self.stop)


    def start_btn_init(self):
        """ 获取所有数据按钮 配置"""
        self.start_btn.setText('获取所有数据')
        self.start_btn.clicked.connect(self.start_btn_slot)

    def xlsx_btn_init(self):
        """获取xlsx按钮 配置"""
        self.xlsx_btn.setText('获取xlsx文档')
        self.xlsx_btn.clicked.connect(self.xlsx_btn_slot)

    def log_browser_init(self):
        """输出文本框 配置"""
        pass

    def progressbar_init(self):
        """进度条"""
        self.progressbar.setRange(0, 10)
        self.progressbar.setValue(0)

    def layout_init(self):
        """页面布局"""
        self.h_layout.addWidget(self.start_btn)
        self.h_layout.addWidget(self.xlsx_btn)

        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addWidget(self.progressbar)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def start_btn_slot(self):
        """获取所有数据"""

        self.xlsx_btn.setEnabled(False)
        self.btn_sound.play()
        self.log_browser.clear()
        self.log_browser.append('<font color="red">获取所有数据</font>')
        self.log_browser.append('<font color="red">下载中...</font>')
        self.config = self.config.Config()
        self.main.run(self.config)
        self.finish_sound.play()
        self.xlsx_btn.setEnabled(True)

    def xlsx_btn_slot(self):
        """获取xlsx汇总文档"""
        self.threads = MyThread()
        self.threads.trigger.connect(self.set_log_slot)  # 进程连接回传到GUI的事件

        self.start_btn.setEnabled(False)
        self.btn_sound.play()
        self.log_browser.clear()
        self.log_browser.append('<font color="red">获取xlsx汇总文档</font>')
        self.log_browser.append('<font color="red">下载中...</font>')
        self.config = self.config.Config(go_img=False)

        # self.threads.start(self.main.run(self.config))
        # self.main.run(self.config)
        self.finish_sound.play()
        self.start_btn.setEnabled(True)

    # def crawl_init(self):
    #     self.threads.trigger.connect(self.set_log_slot)
    #
    def set_log_slot(self, s):
        self.log_browser.append(s)

    def addStdOut(self, st):
        # output = bytes(self.process.readAllStandardOutput()).decode()
        self.log_browser.append(st)


class MyThread(QThread):
    trigger = pyqtSignal(str)

    def __init__(self):
        super(MyThread, self).__init__()

    def __del__(self):
        self.wait()

    def run_(self):
        self.trigger.emit(str('123456'))





def read_qss(style):
    file = QFile(style)
    file.open(QFile.ReadOnly)
    return QTextStream(file).readAll()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrawlWindow()

    qss_style = read_qss(':res/style.qss')
    window.setStyleSheet(qss_style)

    window.show()
    sys.exit(app.exec_())