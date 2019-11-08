# -*- coding: UTF-8 -*-
# @Time    : 2019/6/20 8:51
# @Author  : project
# @File    : GUI.py
# @Software: PyCharm
import os
import sys
import subprocess
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QLineEdit, QComboBox, QMessageBox

import res


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(200, 300)
        self.setWindowTitle('支付宝余额码生成器')
        self.setWindowIcon(QIcon(':reson/maoyan.ico'))

        # 初始化账户名输入文本框
        self.username = QLineEdit(self)
        # 初始化账号输入文本框
        self.account = QLineEdit(self)

        # 初始化启动按钮
        self.start_btn = QPushButton(self)

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
        self.username_init()
        self.account_init()
        self.start_btn_init()
        self.layout_init()

        # 备注名称 账号
        self.bankMark = ''
        self.bankName = ''

    def username_init(self):
        """账户名输入文本框初始化配置"""
        # 设置文本框尺寸
        self.username.setFixedSize(300, 35)
        # 设置默认文本
        self.username.setPlaceholderText("请输入备注名")
        # 限制10个中文字符
        self.username.setMaxLength(10)

    def account_init(self):
        """账号输入文本框初始化配置"""
        self.account.setFixedSize(300, 35)
        # 设置默认文本
        self.account.setPlaceholderText("请输入账号")
        # 限制10个中文字符
        self.account.setMaxLength(30)

    def start_btn_init(self):
        """ 启动按钮按钮 配置"""
        self.start_btn.setText('启动')
        self.start_btn.setEnabled(True)
        self.start_btn.setFixedSize(300, 35)
        self.start_btn.clicked.connect(self.start_btn_slot)

    def set_log_init(self):
        """输出控件 配置"""
        # 输出至输出文本框
        self.worker.log_signal.connect(self.set_log_slot)
        # 调用清屏槽
        self.worker.start_q.connect(self.set_start_slot)

    def layout_init(self):
        """页面布局"""
        # 水平布局
        self.h_layout.addWidget(self.start_btn)
        # 垂直布局
        self.v_layout.addWidget(self.account)
        self.v_layout.addWidget(self.username)
        self.v_layout.addWidget(self.start_btn)

        self.setLayout(self.v_layout)

    def start_btn_slot(self):
        """程序启动"""
        if not self.username.text():
            self.pop_ups('请输入正确的用户名')
            return
        if not self.account.text():
            self.pop_ups('请输入正确的银行卡号')
            return
        self.btn_sound.play()
        self.save_to_txt()
        # self.log_browser.append('<font color="green">{}程序启动{}</font>'.format('*'*20, '*'*20))
        # 启动线程
        self.worker.start()
        self.finish_sound.play()
        self.pop_ups('支付宝余额码生成成功!')

    def pop_ups(self, content):
        """弹窗提示"""
        QMessageBox.information(self, "消息提示", content, QMessageBox.Yes | QMessageBox.No)

    def save_to_txt(self):
        """保存为txt"""
        data = []
        username = self.username.text()
        account = self.account.text()
        data.append(username)
        data.append(account)

        with open('config.txt', 'w+', encoding='utf-8') as f:
            for i in data:
                f.write(i)
                f.write(',')

    def closeEvent(self, event):
        """程序退出确认弹窗"""
        reply = QMessageBox.question(self, '信息', '确认退出吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


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

        # while True:
        try:
            self.start_q.emit(True)
            r = subprocess.Popen(['python', r'spider.py'],  # 需要执行的文件路径
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 bufsize=0)

            while r.poll() is None:
                line = str(r.stdout.readline(), encoding='GBK')  #TODO 打包时改为GBK
                line = line.strip()
                if line:
                    print(line)
                    self.log_data(line)

            # 判断子进程状态
            if r.returncode == 0:
                self.log_signal.emit('<font color="green">Subprogram success</font>')

            else:
                self.log_signal.emit('<font color="red">Subprogram failed</font>')
        except Exception as e:
            # self.log_init().error(e)
            # self.log_init().exception(e)
            os._exit(0)

    def log_data(self, line):
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