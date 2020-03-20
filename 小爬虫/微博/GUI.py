# -*- coding: UTF-8 -*-
# @Time    : 2019/6/20 8:51
# @Author  : project
# @File    : GUI.py
# @Software: PyCharm

import re
import os
import sys
import logging
import subprocess
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextBrowser, QTableWidget, \
    QTableWidgetItem, QHeaderView, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QTextEdit

import res
# 项目路径
PATH = os.getcwd()


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(400, 500)
        self.setWindowTitle('微博关键词搜索')
        self.setWindowIcon(QIcon(':reson/maoyan.ico'))

        # 初始化添加关键字文本框 多行文本框
        self.price = QTextEdit(self)
        # 初始化添加好友按钮
        self.save_combobox = QPushButton(self)
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
        self.combobox_init()
        self.start_btn_init()
        self.layout_init()
        self.set_log_init()

        self.count = True  # 是否清空输入框中的文本

    def movie_init(self):
        """添加关键词输入框默认配置"""
        # 文本框尺寸
        self.price.setFixedSize(300, 100)
        # 设置默认显示文本
        self.price.setPlainText("输入关键词,多个关键词以英文','隔开")
        # 输入内容时清空默认显示文本内容 selectionChanged:点击文本框时发射信号
        self.price.selectionChanged.connect(self.price_clear)

    def price_clear(self):
        """清空输入框中的默认显示文本"""
        if self.count:
            self.price.setPlainText('')
        self.count = False

    def combobox_init(self):
        """添加关键词 按钮 配置"""
        self.save_combobox.setText('添加关键词')
        self.save_combobox.setEnabled(True)
        self.save_combobox.clicked.connect(self.combobox_slot)

    def start_btn_init(self):
        """ 启动按钮按钮 配置"""
        self.start_btn.setText('启动')
        self.start_btn.setEnabled(True)
        # self.start_btn.setFixedSize(300, 30)
        self.start_btn.clicked.connect(self.start_btn_slot)

    def set_log_init(self):
        """输出控件 配置"""
        # 输出至输出文本框
        self.worker.log_signal.connect(self.set_log_slot)
        # 调用清屏槽
        # self.worker.start_q.connect(self.set_start_slot)

    def layout_init(self):
        """页面布局"""
        self.h_layout.addWidget(self.price)
        self.h_layout.addWidget(self.save_combobox)
        self.h_layout.addWidget(self.start_btn)

        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def start_btn_slot(self):
        """程序启动"""
        # 判断填写了关键词 isEnabled():返回控件状态
        if self.save_combobox.isEnabled():
            self.log_browser.append('<font color="red">请填写关键词!!!</font>')
            return None
        self.btn_sound.play()
        self.log_browser.append('<font color="green">{}程序启动{}</font>'.format('*'*20, '*'*20))
        # 启动线程
        self.worker.start()
        # self.finish_sound.play()
        # 设置：按钮状态 输入框 启动
        self.price.setEnabled(False)
        self.save_combobox.setEnabled(False)
        self.start_btn.setEnabled(False)

    def get_words_slot(self):
        """提取输入框中文本"""
        words = self.price.toPlainText()
        if not words or "输入关键词,多个关键词以英文','隔开" in words:
            self.log_browser.append('<font color="red">请正确填写关键词!!!</font>')
            return
        return words

    def combobox_slot(self):
        """关键词输入控件"""
        words = self.get_words_slot()
        if not words:
            return
        # GUI界面输入的关键词写入文件
        self.conf_slot(words)
        # 改变设置按钮状态 输入框 下拉框
        self.price.setEnabled(False)
        self.save_combobox.setEnabled(False)

    def conf_slot(self, words):
        """GUI输入框输入内容保存到配置文件"""
        file = PATH + '\config\words.txt'
        words = words.replace('，', ',').split(',')
        words = [i.replace('\n', '') for i in words if i]
        with open(file, 'w+', encoding='utf-8') as f:
            for i in words:
                f.write(i)
                f.write('\n')
        self.log_browser.append(f'<font color="red">关键词：{words}添加成功</font>')

    def set_log_slot(self, log):
        """添加输出控件显示内容"""
        self.log_browser.append(log)

    def set_start_slot(self):
        """输出框窗口清空"""
        self.log_browser.clear()


class MyThread(QThread):
    log_signal = pyqtSignal(str)
    start_q = pyqtSignal(bool)

    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        # 重写run方法
        # stdout PIPE 输出信息管道（把print信息重定向至管道）
        # stderr STDOUT 错误和日志信息管道
        # bufsize 缓冲设置默认值0 -- 表示不缓冲 1 -- 表示缓冲  NOTE: 如果遇到性能问题，建议将bufsize设置成 -1 或足够大的正数(如 4096）
        # r.poll()   检查子进程状态
        # r.kill()   终止子进程
        # r.send_signal() 向子进程发送信号
        # r.terminate()   终止子进程
        # r.returncode 子进程的退出状态
        # r.stdout.flush() 如果出现子进程假死 管道阻塞 手动刷新缓冲
        try:
            self.start_q.emit(True)
            r = subprocess.Popen(['python', r'spider.py'],  # 需要执行的文件路径
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 bufsize=0)

            while r.poll() is None:
                line = str(r.stdout.readline(), encoding='UTF-8')  # TODO 打包时改为GBK
                line = line.strip()
                if line:
                    self.log_data(line)

            # 判断子进程状态
            if not r.returncode:
                self.log_signal.emit('<font color="green">Subprogram success</font>')
                self.log_signal.emit('<font color="green">程序执行完毕!</font>')

            else:
                self.log_signal.emit('<font color="red">Subprogram failed</font>')
                self.log_signal.emit('<font color="red">程序执行错误!</font>')
        except Exception as e:
            print(e)
            # self.log_init().error(e)
            # self.log_init().exception(e)

    def log_data(self, line):
        # 把管道输出内容传递给显示控件,在GUI界面中显示出来
        self.log_signal.emit(line)


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