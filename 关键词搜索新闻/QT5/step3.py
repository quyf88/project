import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QTextBrowser, QTableWidget, \
                            QTableWidgetItem, QHeaderView, QProgressBar, QHBoxLayout, QVBoxLayout

import requests
from bs4 import BeautifulSoup


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle('猫眼Top100电影爬取软件')
        self.setWindowIcon(QIcon('res/maoyan.png'))

        self.start_btn = QPushButton(self)
        self.stop_btn = QPushButton(self)
        self.save_combobox = QComboBox(self)
        self.table = QTableWidget(self)
        self.log_browser = QTextBrowser(self)
        self.progressbar = QProgressBar(self)

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.crawl_thread = CrawlThread()   # 1

        self.btn_init()
        self.combobox_init()
        self.table_init()
        self.progressbar_init()
        self.layout_init()

    def btn_init(self):
        self.start_btn.setText('开始爬取')
        self.stop_btn.setText('停止爬取')
        self.stop_btn.setEnabled(False)

        self.start_btn.clicked.connect(lambda: self.btn_slot(self.start_btn))
        self.stop_btn.clicked.connect(lambda: self.btn_slot(self.stop_btn))

    def combobox_init(self):
        save_list = ['另存到', 'MySQL', 'csv', 'txt', 'json']
        self.save_combobox.addItems(save_list)
        self.save_combobox.setEnabled(False)

    def table_init(self):
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['图片链接', '电影名称', '主演人员', '上映时间', '电影评分'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def progressbar_init(self):
        self.progressbar.setRange(0, 100)
        self.progressbar.setValue(0)

    def layout_init(self):
        self.h_layout.addWidget(self.start_btn)
        self.h_layout.addWidget(self.stop_btn)
        self.h_layout.addWidget(self.save_combobox)
        self.v_layout.addWidget(self.table)
        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addWidget(self.progressbar)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def btn_slot(self, btn):
        if btn == self.start_btn:
            self.log_browser.clear()
            self.log_browser.append('<font color="red">开始爬取</font>')
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.save_combobox.setEnabled(False)

            self.crawl_thread.start()
        else:
            self.log_browser.append('<font color="red">停止爬取</font>')
            self.stop_btn.setEnabled(False)
            self.start_btn.setEnabled(True)
            self.save_combobox.setEnabled(True)

            self.crawl_thread.terminate()


class CrawlThread(QThread):
    def __init__(self):
        super(CrawlThread, self).__init__()

    def a(self, word):
        print('123')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrawlWindow()
    window.show()
    sys.exit(app.exec_())
