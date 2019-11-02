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
from datetime import datetime
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream, QTimer, QDateTime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextBrowser, QTableWidget, \
    QTableWidgetItem, QHeaderView, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QAbstractItemView, QLabel

import res


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(500, 500)
        self.setWindowTitle('抖音个性签名采集器')
        self.setWindowIcon(QIcon(':reson/maoyan.ico'))

        # 初始化启动按钮
        self.start_btn = QPushButton(self)
        self.start_btn_2 = QPushButton(self)
        self.start_btn_3 = QPushButton(self)
        self.start_btn_4 = QPushButton(self)
        # 初始化表格控件
        self.table = QTableWidget(self)
        # 初始化输出文本框
        self.log_browser = QTextBrowser(self)

        # 初始化水平布局
        self.h_layout = QHBoxLayout()
        self.h1_layout = QHBoxLayout()
        # 初始化垂直布局
        self.v_layout = QVBoxLayout()

        # 初始化音频播放
        self.btn_sound = QSound(':reson/btn.wav', self)
        self.finish_sound = QSound(':reson/finish.wav', self)

        # 实例化线程
        self.worker = MyThread()
        self.worker_2 = MyThread_2()
        self.worker_3 = MyThread_3()
        self.worker_4 = MyThread_4()

        # 实例化
        self.start_btn_init()
        self.start_2_btn_init()
        self.start_3_btn_init()
        self.start_4_btn_init()
        self.table_init()
        self.set_log_init()
        self.layout_init()

        # 读取连接设备
        self.device = None
        self.device_2 = None
        self.device_3 = None
        self.device_4 = None
        self.adb_devices()
        self.datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def start_btn_init(self):
        """ 启动按钮按钮 配置"""
        self.start_btn.setText('启动_1')
        self.start_btn.setEnabled(True)
        # self.start_btn.setFixedSize(300, 30)
        self.start_btn.clicked.connect(self.start_btn_slot)

    def start_2_btn_init(self):
        """ 启动按钮按钮 配置"""
        self.start_btn_2.setText('启动_2')
        self.start_btn_2.setEnabled(True)
        # self.start_btn.setFixedSize(300, 30)
        self.start_btn_2.clicked.connect(self.start_2_btn_slot)

    def start_3_btn_init(self):
        """ 启动按钮按钮 配置"""
        self.start_btn_3.setText('启动_3')
        self.start_btn_3.setEnabled(True)
        # self.start_btn.setFixedSize(300, 30)
        self.start_btn_3.clicked.connect(self.start_3_btn_slot)

    def start_4_btn_init(self):
        """ 启动按钮按钮 配置"""
        self.start_btn_4.setText('启动_4')
        self.start_btn_4.setEnabled(True)
        # self.start_btn.setFixedSize(300, 30)
        self.start_btn_4.clicked.connect(self.start_4_btn_slot)

    def table_init(self):
        """表格控件 配置"""
        # self.table.setFixedSize(500, 250)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['设备', '状态', '运行时间'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置为文本不可编辑

        # 配置默认文本
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem('127.0.0.1'))
        self.table.setItem(row, 1, QTableWidgetItem('未启动'))
        self.table.setItem(row, 2, QTableWidgetItem('0'))

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem('127.0.0.2'))
        self.table.setItem(row, 1, QTableWidgetItem('未启动'))
        self.table.setItem(row, 2, QTableWidgetItem('0'))

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem('127.0.0.3'))
        self.table.setItem(row, 1, QTableWidgetItem('未启动'))
        self.table.setItem(row, 2, QTableWidgetItem('0'))

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem('127.0.0.4'))
        self.table.setItem(row, 1, QTableWidgetItem('未启动'))
        self.table.setItem(row, 2, QTableWidgetItem('0'))

    def set_log_init(self):
        """输出控件 配置"""
        # 输出至输出文本框
        self.worker.log_signal.connect(self.set_log_slot)
        self.worker_2.log_signal.connect(self.set_log_slot)
        self.worker_3.log_signal.connect(self.set_log_slot)
        self.worker_4.log_signal.connect(self.set_log_slot)
        # 输出至表格控件
        # self.worker.result_signal.connect(self.set_table_slot)
        # # 调用清屏槽
        # self.worker.start_q.connect(self.set_start_slot)

    def layout_init(self):
        """页面布局"""
        self.h_layout.addWidget(self.start_btn)
        self.h_layout.addWidget(self.start_btn_2)
        self.h1_layout.addWidget(self.start_btn_3)
        self.h1_layout.addWidget(self.start_btn_4)

        self.v_layout.addWidget(self.table)
        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addLayout(self.h1_layout)
        self.setLayout(self.v_layout)

    def start_btn_slot(self):
        """程序启动"""
        self.btn_sound.play()
        self.log_browser.append('<font color="green">{}程序启动{}</font>'.format('*'*20, '*'*20))
        # 启动线程
        self.worker.start()
        self.finish_sound.play()
        # 改变设置按钮状态为不可点击
        self.start_btn.setEnabled(False)

        # 改变表格窗口文本
        self.table.setItem(0, 0, QTableWidgetItem(self.device))
        self.table.setItem(0, 1, QTableWidgetItem('已启动'))
        self.table.setItem(0, 2, QTableWidgetItem(self.datetime))

    def start_2_btn_slot(self):
        """程序启动"""
        self.btn_sound.play()
        self.log_browser.append('<font color="green">{}程序启动{}</font>'.format('*'*20, '*'*20))
        # 启动线程
        self.worker_2.start()
        self.finish_sound.play()
        # 改变设置按钮状态为不可点击
        self.start_btn_2.setEnabled(False)

    def start_3_btn_slot(self):
        """程序启动"""
        self.btn_sound.play()
        self.log_browser.append('<font color="green">{}程序启动{}</font>'.format('*'*20, '*'*20))
        # 启动线程
        self.worker_3.start()
        self.finish_sound.play()
        # 改变设置按钮状态为不可点击
        self.start_btn_3.setEnabled(False)

    def start_4_btn_slot(self):
        """程序启动"""
        self.btn_sound.play()
        self.log_browser.append('<font color="green">{}程序启动{}</font>'.format('*'*20, '*'*20))
        # 启动线程
        self.worker_4.start()
        self.finish_sound.play()
        # 改变设置按钮状态为不可点击
        self.start_btn_4.setEnabled(False)

    def set_log_slot(self, log):
        self.log_browser.append(log)

    def adb_devices(self):
        """读取设备列表"""
        get_cmd = "adb devices"  # 查询连接设备列表
        count = 0
        try:
            while True:
                # 连接设备
                if count > 2:
                    print("读取设备信息失败,请检查设备是否成功启动")
                    self.log_browser.append('读取设备信息失败,请检查设备是否成功启动')
                    break
                # 读取连接设备信息
                p = subprocess.Popen(get_cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     stdin=subprocess.PIPE, shell=True)

                (output, err) = p.communicate()
                # 分割多条信息为列表
                output = output.decode().replace('\r', '').split('\n')
                # 剔除列表中空字符串
                output = list(filter(None, output))
                if not len(output) > 1:
                    print("读取设备信息失败,自动重启中...")
                    self.log_browser.append('读取设备信息失败,自动重启中...')
                    count += 1
                    continue
                # 连接设备列表
                devices = [i.split('\t') for i in output[1:]]
                # 读取成功列表
                success = [i[0] for i in devices if i[1] == 'device']
                for i in success:
                    print("设备连接成功：[{}]".format(i))
                    self.log_browser.append("设备连接成功：[{}]".format(i))
                break
                # return success
        except:
            print('读取设备信息失败,请检查设备是否成功启动!')
            self.log_browser.append('读取设备信息失败,请检查设备是否成功启动!')
            os._exit(0)

        if len(success) == 1:
            self.device = success[0]
            self.start_btn_2.setEnabled(False)
            self.start_btn_3.setEnabled(False)
            self.start_btn_4.setEnabled(False)
        elif len(success) == 2:
            self.device = success[0]
            self.device_2 = success[1]
            self.start_btn_3.setEnabled(False)
            self.start_btn_4.setEnabled(False)
        elif len(success) == 3:
            self.device = success[0]
            self.device_2 = success[1]
            self.device_3 = success[2]
            self.start_btn_4.setEnabled(False)
        else:
            self.device = success[0]
            self.device_2 = success[1]
            self.device_3 = success[2]
            self.device_4 = success[3]

class MyThread(QThread):
    result_signal = pyqtSignal(str, str, str, str, str, str)
    log_signal = pyqtSignal(str)

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
                r = subprocess.Popen(['python', r'automation.py'],  # 需要执行的文件路径
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     bufsize=0)

                while r.poll() is None:
                    line = str(r.stdout.readline(), encoding='UTF-8')  # TODO 打包时改为GBK
                    line = line.strip()
                    if line:
                        self.log_signal.emit(line)

                # 判断子进程状态
                if r.returncode == 0:
                    self.log_signal.emit('<font color="green">Subprogram success</font>')

                else:
                    self.log_signal.emit('<font color="red">Subprogram failed</font>')
            except Exception as e:
                print(e)


class MyThread_2(QThread):
    result_signal = pyqtSignal(str, str, str, str, str, str)
    log_signal = pyqtSignal(str)

    def __init__(self):
        super(MyThread_2, self).__init__()

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
                r = subprocess.Popen(['python', r'automation.py'],  # 需要执行的文件路径
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     bufsize=0)

                while r.poll() is None:
                    line = str(r.stdout.readline(), encoding='UTF-8')  # TODO 打包时改为GBK
                    line = line.strip()
                    if line:
                        self.log_signal.emit(line)

                # 判断子进程状态
                if r.returncode == 0:
                    self.log_signal.emit('<font color="green">Subprogram success</font>')

                else:
                    self.log_signal.emit('<font color="red">Subprogram failed</font>')
            except Exception as e:
                print(e)


class MyThread_3(QThread):
    result_signal = pyqtSignal(str, str, str, str, str, str)
    log_signal = pyqtSignal(str)

    def __init__(self):
        super(MyThread_3, self).__init__()

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
                r = subprocess.Popen(['python', r'automation.py'],  # 需要执行的文件路径
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     bufsize=0)

                while r.poll() is None:
                    line = str(r.stdout.readline(), encoding='UTF-8')  # TODO 打包时改为GBK
                    line = line.strip()
                    if line:
                        self.log_signal.emit(line)

                # 判断子进程状态
                if r.returncode == 0:
                    self.log_signal.emit('<font color="green">Subprogram success</font>')

                else:
                    self.log_signal.emit('<font color="red">Subprogram failed</font>')
            except Exception as e:
                print(e)


class MyThread_4(QThread):
    result_signal = pyqtSignal(str, str, str, str, str, str)
    log_signal = pyqtSignal(str)

    def __init__(self):
        super(MyThread_4, self).__init__()

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
                r = subprocess.Popen(['python', r'automation.py'],  # 需要执行的文件路径
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     bufsize=0)

                while r.poll() is None:
                    line = str(r.stdout.readline(), encoding='UTF-8')  # TODO 打包时改为GBK
                    line = line.strip()
                    if line:
                        self.log_signal.emit(line)

                # 判断子进程状态
                if r.returncode == 0:
                    self.log_signal.emit('<font color="green">Subprogram success</font>')

                else:
                    self.log_signal.emit('<font color="red">Subprogram failed</font>')
            except Exception as e:
                print(e)


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
