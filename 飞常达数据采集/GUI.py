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
    QTableWidgetItem, QHeaderView, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox

import res


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle('机场航班信息实时监测')
        self.setWindowIcon(QIcon(':reson/maoyan.ico'))

        # 初始化添加推送好友文本框
        self.price = QLineEdit(self)
        # 初始化添加好友按钮
        self.save_combobox = QPushButton(self)
        # 初始化启动按钮
        self.start_btn = QPushButton(self)
        # 初始化表格控件
        self.table = QTableWidget(self)
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
        self.table_init()
        self.set_log_init()

    def movie_init(self):
        """添加好友输入框默认配置"""
        # 设置文本框尺寸
        self.price.setFixedSize(300, 30)
        # 设置默认文本
        self.price.setPlaceholderText("输入好友备注名称,多个好友以英文','隔开")
        # 默认设置不可输入
        # self.price.setEnabled(False)
        # 限制10个中文字符
        self.price.setMaxLength(100)

    def combobox_init(self):
        """添加好友 按钮 配置"""
        self.save_combobox.setText('添加推送好友')
        self.save_combobox.setEnabled(True)
        self.save_combobox.clicked.connect(self.combobox_slot)

    def start_btn_init(self):
        """ 启动按钮按钮 配置"""
        self.start_btn.setText('启动')
        self.start_btn.setEnabled(True)
        # self.start_btn.setFixedSize(300, 30)
        self.start_btn.clicked.connect(self.start_btn_slot)

    def table_init(self):
        """表格控件 配置"""
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['机场', '航班', '计划起飞', '出发地', '目的地', '延误时间'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def set_log_init(self):
        """输出控件 配置"""
        # 输出至输出文本框
        self.worker.log_signal.connect(self.set_log_slot)
        # 输出至表格控件
        self.worker.result_signal.connect(self.set_table_slot)
        # 调用清屏槽
        self.worker.start_q.connect(self.set_start_slot)

    def layout_init(self):
        """页面布局"""
        self.h_layout.addWidget(self.price)
        self.h_layout.addWidget(self.save_combobox)
        self.h_layout.addWidget(self.start_btn)

        self.v_layout.addWidget(self.table)
        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def start_btn_slot(self):
        """程序启动"""

        self.btn_sound.play()
        self.log_browser.append('<font color="green">{}程序启动{}</font>'.format('*'*20, '*'*20))
        # 启动线程
        self.worker.start()
        self.finish_sound.play()
        # 改变设置按钮状态 输入框 下拉框
        self.price.setEnabled(False)
        self.save_combobox.setEnabled(False)
        self.start_btn.setEnabled(False)

    def combobox_slot(self):
        """添加好友"""
        if not self.price.text():
            self.log_browser.append('<font color="red">请填写好友备注名称</font>')
            return
        self.conf_slot(self.price.text())

    def conf_slot(self, friend):
        """配置文件"""
        path = os.path.abspath('.') + '\config\config.txt'
        friend = friend.split(',')
        with open(path, 'a+', encoding='utf-8') as f:
            for i in friend:
                f.write(i)
                f.write('\n')
        if friend:
            self.log_browser.append('<font color="red">添加推送新成员：[{}]成功</font>'.format(friend))
        # 改变设置按钮状态 输入框 下拉框
        self.price.setEnabled(False)
        self.save_combobox.setEnabled(False)

    def set_log_slot(self, log):
        self.log_browser.append(log)

    def set_table_slot(self, airport, flight, plan_time, departure, destination, mora_time):
        """表格控件输出"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(airport))
        self.table.setItem(row, 1, QTableWidgetItem(flight))
        self.table.setItem(row, 2, QTableWidgetItem(plan_time))
        self.table.setItem(row, 3, QTableWidgetItem(departure))
        self.table.setItem(row, 4, QTableWidgetItem(destination))
        self.table.setItem(row, 5, QTableWidgetItem(mora_time))

    def set_start_slot(self):
        # 表格清空 输出框窗口清空
        # self.table.clearContents()
        # self.table.setRowCount(0)
        self.log_browser.clear()


class MyThread(QThread):
    result_signal = pyqtSignal(str, str, str, str, str, str)
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

        while True:
            try:
                self.start_q.emit(True)
                r = subprocess.Popen(['python', r'Login.py'],  # 需要执行的文件路径
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     bufsize=0)

                while r.poll() is None:
                    line = str(r.stdout.readline(), encoding='GBK')  #TODO 打包时改为GBK
                    line = line.strip()
                    if line:
                        self.log_data(line)

                # 判断子进程状态
                if r.returncode == 0:
                    self.log_signal.emit('<font color="green">Subprogram success</font>')

                else:
                    self.log_signal.emit('<font color="red">Subprogram failed</font>')
            except Exception as e:
                self.log_init().error(e)
                self.log_init().exception(e)

    def log_data(self, line):
        if 'content' in line:
            airport, flight, plan_time, departure, destination, mora_time = re.findall(r'\[.*?]', line)
            airport = (re.sub(r'[(\[)(\])]', '', airport))
            flight = (re.sub(r'[(\[)(\])]', '', flight))
            plan_time = (re.sub(r'[(\[)(\])]', '', plan_time))
            departure = (re.sub(r'[(\[)(\])]', '', departure))
            destination = (re.sub(r'[(\[)(\])]', '', destination))
            mora_time = (re.sub(r'[(\[)(\])]', '', mora_time))
            self.result_signal.emit(airport, flight, plan_time, departure, destination, mora_time)

        self.log_signal.emit(line)

    def log_init(self):
        """日志模块"""
        path = os.path.abspath('.') + r'\log\GUI.log'
        formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        fh = logging.FileHandler(path, encoding='utf-8', mode='a+')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        console.setFormatter(formatter)
        # 如果需要同時需要在終端上輸出，定義一個streamHandler
        # print_handler = logging.StreamHandler()  # 往屏幕上输出
        # print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
        logger = logging.getLogger("GUI")
        # logger.addHandler(print_handler)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console)
        logger.addHandler(fh)
        return logger


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