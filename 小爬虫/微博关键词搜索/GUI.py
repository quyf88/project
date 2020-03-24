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
from configparser import ConfigParser

from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextBrowser, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QTextEdit, QCheckBox, QMessageBox

import res


# 项目路径
PATH = os.getcwd()


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(400, 500)
        self.setWindowTitle('微博关键词搜索')
        self.setWindowIcon(QIcon(':reson/maoyan.ico'))

        # 初始化输出文本框
        self.log_browser = QTextBrowser(self)
        # 初始化添加关键字文本框 多行文本框
        self.price = QTextEdit(self)
        # 初始化添加好友按钮
        self.save_combobox = QPushButton(self)
        # 初始化启动按钮
        self.start_btn = QPushButton(self)
        # 初始化暂停按钮
        self.stop = QPushButton(self)
        # 初始化IP代理复选框
        self.checkbox = QCheckBox('启用代理', self)
        # 初始化多线程复选框
        self.start_thread = QCheckBox('启用多线程', self)

        # 界面布局 全局控件（注意参数self），用于承载全局布局
        wwg = QWidget(self)
        self.w_layout = QHBoxLayout(wwg)  # 初始化全局布局为水平模式(全局布局)
        self.h_layout = QHBoxLayout()  # 初始化水平布局(局部布局)
        self.v_layout = QVBoxLayout()  # 初始化垂直布局(局部布局)
        self.g_layout = QGridLayout()  # 初始化网格布局(局部布局)
        # self.f_layout = QFormLayout()  # 初始化表单布局(局部布局)

        # 初始化音频播放
        self.btn_sound = QSound(':reson/btn.wav', self)
        self.finish_sound = QSound(':reson/finish.wav', self)

        # 实例化线程
        self.worker = MyThread()

        # 实例化控件默认配置
        self.movie_init()  # 关键词
        self.combobox_init()  # 添加关键词按钮
        self.start_btn_init()  # 启动按钮
        self.stop_init()  # 暂停按钮
        self.layout_init()  # 页面布局
        self.set_log_init()  # 输出控件
        self.checkbox_init()  # IP代理复选框
        self.start_thread_init()  # 启用多线程代理复选框

        self.ini_init()  # 初始化配置文件参数
        self.count = True  # 是否清空输入框中的文本

    def ini_init(self):
        """config.ini 配置文件初始化"""
        self.log_browser.append('GUI界面启动中...')
        self.log_browser.append('GUI界面启动成功')
        self.log_browser.append('检查配置文件...')
        self.log_browser.append('初始化配置文件')
        self.red_ini('Status', 'proxy', '0')  # 设置IP代理为不可用
        self.red_ini('Status', 'thread', '0')  # 设置多线程关闭
        self.red_ini('Words', 'words', 'None')  # 设置关键词为空
        self.log_browser.append('初始化配置文件成功')
        self.log_browser.append('<font color="green">系统启动成功,请添加搜索关键词</font>')

    def movie_init(self):
        """添加关键词输入框 初始化配置"""
        # 文本框尺寸
        self.price.setFixedSize(220, 100)
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
        """添加关键词按钮 初始化配置"""
        self.save_combobox.setText('添加关键词')
        self.save_combobox.setEnabled(True)
        self.save_combobox.clicked.connect(self.combobox_slot)

    def start_btn_init(self):
        """启动按钮 初始化配置"""
        self.start_btn.setText('启动')
        self.start_btn.setEnabled(True)
        # self.start_btn.setFixedSize(300, 30)
        self.start_btn.clicked.connect(self.start_btn_slot)

    def stop_init(self):
        """暂停按钮 初始化配置"""
        self.stop.setText('停止')
        self.stop.setEnabled(False)
        self.stop.clicked.connect(self.stop_slot)

    def set_log_init(self):
        """输出控件 初始化配置"""
        # 输出至输出文本框
        self.worker.log_signal.connect(self.set_log_slot)
        # 调用清屏槽
        # self.worker.start_q.connect(self.set_start_slot)
        # 改变按钮状态
        self.worker.start_q.connect(self.set_enabled_slot)

    def checkbox_init(self):
        """IP代理复选框 初始化配置"""
        # 复选框默认选中
        # self.checkbox.toggle()
        self.checkbox.stateChanged.connect(self.checkbox_slot)

    def start_thread_init(self):
        """开启多线程复选框 初始化配置"""
        self.start_thread.stateChanged.connect(self.start_thread_slot)

    def layout_init(self):
        """页面布局"""
        # 输出控件设置为垂直布局方式
        self.v_layout.addWidget(self.log_browser)

        # 局部布局 关键词输入控件、添加关键词按钮、启动按钮、暂停按钮 水平布局+网格布局方式
        self.h_layout.addWidget(self.price)  # 关键词输入控件设置为水平布局
        self.g_layout.addWidget(self.save_combobox, 1, 0)  # 添加关键词按钮设置为网格布局指定位置为第一行第一个位置
        self.g_layout.addWidget(self.start_thread, 0, 0)
        self.g_layout.addWidget(self.checkbox, 0, 1)
        self.g_layout.addWidget(self.start_btn, 2, 0)  # 启动按钮设置为网格布局指定位置为第二行第一个位置
        self.g_layout.addWidget(self.stop, 2, 1)  # 暂停按钮设置为网格布局指定职位只第二行第二个位置
        self.h_layout.addLayout(self.g_layout)  # 将局部网格布局嵌套进局部水平布局(关键词输入控件、添加关键词按钮、启动按钮、暂停按钮 绑定在一起)
        self.v_layout.addLayout(self.h_layout)  # 将局部水平布局嵌套进局部垂直布局(将上一步整合的布局和输出控件平级,设置成垂直布局)

        # 将局部布局添加到全局布局中
        self.w_layout.addLayout(self.v_layout)
        # 将布局应用到窗口
        self.setLayout(self.w_layout)

    def start_btn_slot(self):
        """程序启动 信号槽"""
        # 判断添加关键词 按钮状态, True:可按，False:不可按。 isEnabled():返回控件状态
        if self.save_combobox.isEnabled():
            self.log_browser.append('<font color="red">请填写关键词!!!</font>')
            return None
        self.btn_sound.play()
        self.log_browser.append('<font color="green">{}程序启动{}</font>'.format('*'*20, '*'*20))
        # 启动线程
        self.worker.start()
        # self.finish_sound.play()
        # 初始化各个按钮状态
        self.price.setEnabled(False)  # 输入框
        self.save_combobox.setEnabled(False)  # 添加关键字按钮
        self.checkbox.setEnabled(False)  # IP代理复选框
        self.start_thread.setEnabled(False)  # 开启多线程复选框
        self.start_btn.setEnabled(False)  # 启动按钮
        self.stop.setEnabled(True)  # 暂停按钮

    def stop_slot(self):
        """暂停 信号槽"""
        # 改变程序状态
        self.worker.stop = True
        # 改变各按钮状态
        self.price.setEnabled(True)  # 输入框
        self.save_combobox.setEnabled(True)  # 添加关键字按钮
        self.checkbox.setEnabled(True)  # IP代理复选框
        self.start_thread.setEnabled(True)  # 开启多线程复选框
        self.start_btn.setEnabled(True)  # 启动按钮
        self.stop.setEnabled(False)  # 暂停按钮

    def combobox_slot(self):
        """关键词输入控件 信号槽"""
        words = self.get_words()
        if not words:
            return
        # GUI界面输入的关键词写入文件
        words = words.replace('，', ',').replace('\n', '')
        val = self.red_ini('Words', 'words', words)
        self.log_browser.append(f'<font color="green">关键词：[{val}]添加成功</font>')
        # 改变设置按钮状态 输入框 添加关键词按钮
        self.price.setEnabled(False)
        self.save_combobox.setEnabled(False)

    def get_words(self):
        """提取输入框文本信息 信号槽"""
        words = self.price.toPlainText()
        if not words or "输入关键词,多个关键词以英文','隔开" in words:
            self.log_browser.append('<font color="red">请正确填写关键词!!!</font>')
            return
        return words

    def checkbox_slot(self):
        """IP代理复选框 信号槽"""
        if self.checkbox.isChecked():
            self.red_ini('Status', 'proxy', '1')
            self.log_browser.append('<font color="green">开启IP代理成功</font>')
            return None
        self.red_ini('Status', 'proxy', '0')
        self.log_browser.append('<font color="red">关闭IP代理成功</font>')

    def start_thread_slot(self):
        """开启多线程复选框 信号槽"""
        if self.start_thread.isChecked():
            self.red_ini('Status', 'thread', '1')
            self.log_browser.append('<font color="green">开启多线程</font>')
            return None
        self.red_ini('Status', 'thread', '0')
        self.log_browser.append('<font color="red">关闭多线程</font>')

    def set_enabled_slot(self, status):
        """子程序结束改变按钮状态"""
        if not status:
            self.price.setEnabled(True)  # 输入框
            self.save_combobox.setEnabled(True)  # 添加关键字按钮
            self.checkbox.setEnabled(True)  # IP代理
            self.start_thread.setEnabled(True)  # 开启多线程复选框
            self.start_btn.setEnabled(True)  # 启动按钮
            self.stop.setEnabled(False)  # 暂停按钮

    def set_log_slot(self, log):
        """添加输出控件显示内容 信号槽"""
        self.log_browser.append(log)

    def set_start_slot(self):
        """输出框窗口清空 信号槽"""
        self.log_browser.clear()

    def red_ini(self, section, name, val):
        """读取、修改 ini配置文件"""
        file = PATH + '\config\config.ini'  # 文件路径
        cp = ConfigParser()  # 实例化
        cp.read(file, encoding='utf-8')  # 读取文件
        cp.set(section, name, val)  # 修改数据
        # 写入新数据
        with open(file, 'w', encoding='utf-8') as f:
            cp.write(f)

        # 读取修改后数据
        val = cp.get(section, name)
        return val

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
    stop = False  # 是否终止程序

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
            self.stop = False
            self.start_q.emit(True)
            r = subprocess.Popen(['python', r'spider.py'],  # 需要执行的文件路径
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 bufsize=0)

            while r.poll() is None:
                # 判断是否终止子程序(调用的程序)
                if self.stop:
                    r.terminate()  # win10终止子进程
                    self.log_signal.emit('<font color="red">*****程序已关闭*****</font>')
                    return
                line = str(r.stdout.readline(), encoding='UTF-8')  # TODO 打包时改为GBK
                line = line.strip()
                if line:
                    self.log_data(line)

            # 判断子进程状态
            if not r.returncode:
                self.log_signal.emit('<font color="green">Subprogram success</font>')
                self.log_signal.emit('<font color="green">程序执行完毕!</font>')
                self.start_q.emit(False)
            else:
                self.log_signal.emit('<font color="red">Subprogram failed</font>')
                self.log_signal.emit('<font color="red">程序执行错误!</font>')
                self.start_q.emit(False)
        except Exception as e:
            print(e)
            self.start_q.emit(False)
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