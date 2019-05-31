import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QTextBrowser, QTableWidget, \
    QTableWidgetItem, QHeaderView, QProgressBar, QHBoxLayout, QVBoxLayout, QMessageBox, QLineEdit

import json
import csv
from 关键词搜索新闻.QT5.cloud import Cloud
from 关键词搜索新闻.QT5.get_news import SearchNews
from 关键词搜索新闻.QT5.get_comment import GetComment
from 关键词搜索新闻.QT5 import res


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle('关键词新闻搜索')
        self.setWindowIcon(QIcon(':res/4.jpg'))

        # 初始化搜索文本框
        self.movie_name = QLineEdit(self)
        # 初始化渠道下拉框
        self.source_combobox = QComboBox(self)
        # 初始化一键搜索按钮
        self.start_btn = QPushButton(self)
        # 初始化开始爬取按钮
        self.get_btn = QPushButton(self)
        # 初始化一键分析按钮
        self.word_cloud = QPushButton(self)
        # 初始化另存下拉框
        self.save_combobox = QComboBox(self)
        # 初始化表格控件
        self.table = QTableWidget(self)
        # 初始化输出文本框
        self.log_browser = QTextBrowser(self)
        # 初始化进度条
        self.progressbar = QProgressBar(self)

        # 初始化水平布局
        self.h_layout = QHBoxLayout()
        # 初始化垂直布局
        self.v_layout = QVBoxLayout()

        # 实例化词云程序
        self.cloud = Cloud()
        # 实例化启动程序
        self.crawl_thread = CrawlThread()
        # 初始化数据库
        self.db = None
        # 初始化音频播放
        self.btn_sound = QSound(':res/btn.wav', self)
        self.finish_sound = QSound(':res/finish.wav', self)

        # 实例化
        self.movie_init()
        self.source_init()
        self.btn_init()
        self.combobox_init()
        self.table_init()
        self.word_cloud_init()
        self.log_init()
        self.progressbar_init()
        self.layout_init()
        self.crawl_init()
        self.db_connect()

    def movie_init(self):
        """搜索文本框默认配置"""
        # 设置文本框尺寸
        self.movie_name.setFixedSize(200, 25)
        # 设置默认文本
        self.movie_name.setPlaceholderText("请输入关键词,不超过十个中文")
        # 限制10个中文字符
        self.movie_name.setMaxLength(10)

    def source_init(self):
        """搜索渠道下拉框配置"""
        save_list = ['搜索渠道选择', '新华网', '新浪新闻', '百度新闻']
        self.source_combobox.addItems(save_list)
        # 设置标签状态为可用
        self.source_combobox.setEnabled(True)

        #  当下拉索引发生改变时发射信号触发绑定的事件
        # self.source_combobox.currentTextChanged.connect(self.combobox_slot)

    def btn_init(self):
        self.start_btn.setText('一键搜索')
        self.get_btn.setText('开始爬取')
        self.get_btn.setEnabled(False)

        self.start_btn.clicked.connect(lambda: self.btn_slot(self.start_btn))
        self.get_btn.clicked.connect(lambda: self.btn_slot(self.get_btn))

    # TODO
    def word_cloud_init(self):
        """一键分析配置"""
        self.word_cloud.setText('一键分析')
        self.word_cloud.setEnabled(False)
        self.word_cloud.clicked.connect(self.word_cloud_slot)

    def combobox_init(self):
        """另存为下拉框配置"""
        save_list = ['另存为', 'MySQL', 'csv', 'txt', 'json']
        self.save_combobox.addItems(save_list)
        # 设置标签状态为不可用
        self.save_combobox.setEnabled(False)

        #  当下拉索引发生改变时发射信号触发绑定的事件
        self.save_combobox.currentTextChanged.connect(self.combobox_slot)  # 1

    def table_init(self):
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['新闻链接', '评论信息', '渠道来源', '发布日期'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def log_init(self):
        """输出文本框配置"""
        # 设置盒子尺寸
        self.log_browser.setFixedSize(800, 150)

    def progressbar_init(self):
        """进度条"""
        self.progressbar.setRange(0, 10)
        self.progressbar.setValue(0)

    def layout_init(self):
        """页面布局"""
        self.h_layout.addWidget(self.movie_name)
        self.h_layout.addWidget(self.source_combobox)
        self.h_layout.addWidget(self.start_btn)
        self.h_layout.addWidget(self.get_btn)
        self.h_layout.addWidget(self.word_cloud)
        self.h_layout.addWidget(self.save_combobox)

        self.v_layout.addWidget(self.table)
        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addWidget(self.progressbar)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def crawl_init(self):
        self.crawl_thread.total_nums.connect(self.total_nums_slot)
        self.crawl_thread.finished_signal.connect(self.finish_slot)
        self.crawl_thread.log_signal.connect(self.set_log_slot)
        self.crawl_thread.result_signal.connect(self.set_table_slot)

    def btn_slot(self, btn):
        self.btn_sound.play()
        # 点击一键搜索
        if btn == self.start_btn:
            # 判断是否输入关键词
            if self.movie_name.text():
                self.log_browser.clear()
                self.log_browser.append('<font color="red">一键搜索</font>')
                self.log_browser.append('<font color="red">搜索中...</font>')
                self.table.clearContents()
                self.table.setRowCount(0)
                self.get_btn.setEnabled(True)
                self.save_combobox.setEnabled(False)

                self.crawl_thread.render(self.movie_name, self.source_combobox)
                self.crawl_thread.start()
            else:
                self.log_browser.append('<font color="red">请输入搜索关键词!</font>')

        if btn == self.get_btn:
            self.log_browser.append('<font color="red">开始爬取</font>')
            self.get_btn.setEnabled(False)
            self.start_btn.setEnabled(True)
            self.word_cloud.setEnabled(True)
            self.save_combobox.setEnabled(True)

            self.run()

    def word_cloud_slot(self):
        self.cloud.run()

    def total_nums_slot(self, total_nums):
        """搜索到新闻数"""
        total_nums = '本次搜索总找到新闻：{}条'.format(total_nums)
        self.log_browser.append(total_nums)

    def finish_slot(self):
        self.start_btn.setEnabled(True)
        self.get_btn.setEnabled(False)
        self.save_combobox.setEnabled(True)

    def set_log_slot(self, new_log):
        self.log_browser.append(new_log)

    def set_table_slot(self, img, name, star, time):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(img))
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.table.setItem(row, 2, QTableWidgetItem(star))
        self.table.setItem(row, 3, QTableWidgetItem(time))

    def combobox_slot(self, text):
        if text == 'MySQL':
            self.save_to_MySQL()
        elif text == 'csv':
            self.save_to_csv()
        elif text == 'txt':
            self.save_to_txt()
        elif text == 'json':
            self.save_to_json()

    def db_connect(self):
        """
        SQL配置
        db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        db.setHostName('主机名')
        db.setDatabaseName('数据库名')
        db.setUserName('用户名')
        db.setPassword('密码')
        db.setPort(3306) # 端口号
        db.open() # 判断是否连接数据库成功 返回布尔值
        """
        # 创建数据库连接并打开
        self.db = QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName('localhost')
        self.db.setDatabaseName('news')
        self.db.setUserName('root')
        self.db.setPassword('raspberry')
        if not self.db.open():
            QMessageBox.critical(self, 'Database Connection', self.db.lastError().text())

    def closeEvent(self, QCloseEvent):
        self.db.close()

    def save_to_MySQL(self):
        query = QSqlQuery()

        # query.exec_("CREATE TABLE IF NOT EXISTS movie "
        #             "(img VARCHAR(100), name VARCHAR(50), star VARCHAR(100),"
        #             " time VARCHAR(50), score VARCHAR(5))")

        for row in range(self.table.rowCount()):
            word = self.movie_name.text()
            img = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            star = self.table.item(row, 2).text()
            time = self.table.item(row, 3).text()
            query.prepare("INSERT INTO words (keyword,new_url,new_tag,new_summary,source) "
                          "VALUES (?, ?, ?, ?, ?)")
            # sql = 'insert into words(keyword,new_url,new_tag,new_summary,source) VALUES ' \
            #       '(%(keyword)s,%(url)s,%(tag)s,%(summary)s,%(source)s)'
            # query.bindValue(0, word)
            # query.bindValue(1, img)
            # query.bindValue(2, name)
            # query.bindValue(3, star)
            # query.bindValue(4, time)
            query.addBindValue(word)
            query.addBindValue(img)
            query.addBindValue(name)
            query.addBindValue(star)
            query.addBindValue(time)

            query.exec_()

        QMessageBox.information(self, '保存到MySQL', '保存成功！', QMessageBox.Ok)

    def save_to_csv(self):
        """保存为scv文件"""
        content = []
        for row in range(self.table.rowCount()):
            img = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            star = self.table.item(row, 2).text()
            time = self.table.item(row, 3).text()
            content.append([img, name, star, time])

        with open('./关键词搜索.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['新闻链接', '渠道来源', '发布日期', '新闻摘要'])
            writer.writerows(content)

        QMessageBox.information(self, '保存到csv', '保存成功！', QMessageBox.Ok)

    def save_to_txt(self):
        """保存为txt"""
        content = ''
        for row in range(self.table.rowCount()):
            img = '新闻链接：{}\n'.format(self.table.item(row, 0).text())
            name = '渠道来源：{}\n'.format(self.table.item(row, 1).text())
            star = '发布日期：{}\n'.format(self.table.item(row, 2).text())
            time = '新闻摘要：{}\n'.format(self.table.item(row, 3).text())

            content += img + name + star + time + '\n'

        with open('./关键词搜索新闻.txt', 'w', encoding='utf-8') as f:
            f.write(content)

        QMessageBox.information(self, '保存到txt', '保存成功！', QMessageBox.Ok)

    def save_to_json(self):
        """保存为json文件"""
        content = []
        for row in range(self.table.rowCount()):
            img = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            star = self.table.item(row, 2).text()
            time = self.table.item(row, 3).text()
            content.append(
                {
                    '新闻链接': img,
                    '渠道来源': name,
                    '发布日期': star,
                    '新闻摘要': time,
                }
            )

        with open('./关键词搜索新闻.json', 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False)

        QMessageBox.information(self, '保存到json', '保存成功！', QMessageBox.Ok)

    def run(self):
        """根据url爬取数据"""

        for row in range(self.table.rowCount()):
            new_url = self.table.item(row, 0).text()
            self.log_browser.append('开始爬取:{}'.format(new_url))

            self.progressbar.setValue(row + 1)
            if self.progressbar.value() == 10:
                self.finish_sound.play()
        self.log_browser.append('<font color="red">全部爬取完毕！</font>')


class CrawlThread(QThread):
    search_news = SearchNews()
    comment = GetComment()
    total_nums = pyqtSignal(str)
    finished_signal = pyqtSignal()
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(str, str, str, str)

    def __init__(self):
        super(CrawlThread, self).__init__()

    def render(self, movie_name, source_combobox):
        word = movie_name.text()
        source = source_combobox.currentText()
        message = self.comment.comment_message(word)
        if source == self.tr('新华网'):
            data = self.search_news.xinhua_news(word)
        elif source == self.tr('新浪新闻'):
            data = self.search_news.sina_news(word)
        elif source == self.tr('百度新闻'):
            data = self.search_news.baidu_news(word)
        else:
            data = None

        try:
            total, url_list, pubtime_list, sitename_list, summary_list, source = data

            self.total_nums.emit(str(total))
            for i in range(len(url_list)):
                self.result_signal.emit(str(url_list[i]), str(next(message)), str(sitename_list[i]),  str(pubtime_list[i]))

        except Exception as e:
            self.log_signal.emit('<font color="red">状态码返回错误，请求失败请重试!</font>')
            self.log_signal.emit(e)


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
