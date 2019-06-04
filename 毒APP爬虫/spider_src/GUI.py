# -*- coding: utf-8 -*-
# @Time    : 2019/6/4 8:51
# @Author  : project
# @File    : 测试测试.py
# @Software: PyCharm
import multiprocessing
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout

import res
import main
import config


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(300, 150)
        self.setWindowTitle('毒APP数据采集')
        self.setWindowIcon(QIcon(':reson/maoyan.ico'))

        # 初始化获取所有数据按钮
        self.start_btn = QPushButton(self)
        # 初始化获取xlsx按钮
        self.xlsx_btn = QPushButton(self)
        # 初始化输出文本框
        # self.log_browser = QTextBrowser(self)

        # 初始化水平布局
        self.h_layout = QHBoxLayout()
        # 初始化垂直布局
        self.v_layout = QVBoxLayout()

        # 初始化音频播放
        self.btn_sound = QSound(':reson/btn.wav', self)
        self.finish_sound = QSound(':reson/finish.wav', self)

        # 实例化线程
        self.threads = MyThread()
        # self.worker = MyThread()
        self.config = None

        # 实例化
        self.start_btn_init()
        self.xlsx_btn_init()
        self.layout_init()

    def start_btn_init(self):
        """ 获取所有数据按钮 配置"""
        self.start_btn.setText('获取所有数据')
        self.start_btn.clicked.connect(self.start_btn_slot)

    def xlsx_btn_init(self):
        """获取xlsx按钮 配置"""
        self.xlsx_btn.setText('获取xlsx文档')
        self.xlsx_btn.clicked.connect(self.xlsx_btn_slot)

    def layout_init(self):
        """页面布局"""
        self.h_layout.addWidget(self.start_btn)
        self.h_layout.addWidget(self.xlsx_btn)

        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def start_btn_slot(self):
        """获取所有数据"""

        self.btn_sound.play()
        print('<font color="red">获取所有数据</font>')
        print('<font color="red">下载中...</font>')
        self.threads.download_img(True)
        self.threads.start()
        # self.threads.waitForFinished(-1)
        self.finish_sound.play()
        self.start_btn.setEnabled(False)
        self.xlsx_btn.setEnabled(False)

    def xlsx_btn_slot(self):
        """获取xlsx汇总文档"""

        self.start_btn.setEnabled(False)
        self.xlsx_btn.setEnabled(False)
        self.btn_sound.play()
        print('<font color="red">获取xlsx汇总文档</font>')
        print('<font color="red">下载中...</font>')
        self.threads.download_img(False)
        self.threads.start()
        # self.threads.waitForFinished(-1)  # TODO
        self.finish_sound.play()
        self.start_btn.setEnabled(False)
        self.xlsx_btn.setEnabled(False)
    # def worker_thread(self):
    #     """子线程"""
    #
    #     thread = QThread()
    #     thread.setObjectName('thread_')
    #     # 实例化对象绑定子线程
    #     self.worker.moveToThread(thread)
    #     # 绑定信号槽
    #     # worker.trigger.connect()
    #     # start 启动一个线程 ；绑定信号 started() 至某个槽函数上，当线程开始执行后会发出信号
    #     thread.started.connect(self.worker.main_run)
    #     thread.start()


class MyThread(QThread):
    config = None
    _run_main = main
    trigger = pyqtSignal()

    def __init__(self):
        super(MyThread, self).__init__()

    def download_img(self, download=None):
        if download:
            self.config = config.Config(go_img=True)
        else:
            self.config = config.Config(go_img=False)

    def run(self):
        # 重写父类run 启动子进程
        self._run_main.run(self.config)


def read_qss(style):
    file = QFile(style)
    file.open(QFile.ReadOnly)
    return QTextStream(file).readAll()


if __name__ == '__main__':
    # 解决多线程打包问题
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = CrawlWindow()
    qss_style = read_qss(':reson/style.qss')
    window.setStyleSheet(qss_style)
    window.show()
    sys.exit(app.exec_())

