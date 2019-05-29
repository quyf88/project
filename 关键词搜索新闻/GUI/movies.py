# -*- encoding:utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from 关键词搜索新闻.GUI import helpUI
from 关键词搜索新闻.GUI.movieSource.MovieHeaven import MovieHeaven
from 关键词搜索新闻.get_news import SearchNews

QTextCodec.setCodecForTr(QTextCodec.codecForName('utf8'))


class LayoutDialog(QDialog, helpUI.Ui_Dialog):
    __slots__ = ['word', 'movie_name_label', 'movie_name_line_edit', 'movie_source_label', 'movie_source_combobox',
                 'search_push_button', 'tip_label', 'search_content_label', 'search_content_text_list']

    def __init__(self, parent=None):
        super(LayoutDialog, self).__init__(parent)
        self.setupUi(self)
        self.work = WorkThread()

        self.setWindowTitle(self.tr("Search Movies"))
        self.setWindowIcon(QIcon('./searchMovies.ico'))

        self.movie_name_label = QLabel(self.tr("搜索关键词:"))
        self.movie_name_line_edit = QLineEdit()  # 实例化一个输入框

        self.movie_source_label = QLabel(self.tr("渠道:"))
        self.movie_source_combobox = QComboBox()
        self.movie_source_combobox.addItem(self.tr('新华网'))
        self.movie_source_combobox.addItem(self.tr('新浪新闻'))
        self.movie_source_combobox.addItem(self.tr('百度新闻'))

        self.search_push_button = QPushButton(self.tr("搜索"))

        self.tip_label = QLabel(self.tr("未开始查询..."))
        self.search_content_label = QLabel(self.tr("查询内容:"))
        self.search_content_text_list = QListWidget()  # 实例化一个(item base)的列表

        top_layout = QGridLayout()
        top_layout.addWidget(self.movie_name_label, 0, 0)
        top_layout.addWidget(self.movie_name_line_edit, 0, 1)
        top_layout.addWidget(self.movie_source_label, 0, 2)
        top_layout.addWidget(self.movie_source_combobox, 0, 3)
        top_layout.addWidget(self.search_push_button, 0, 4)
        top_layout.addWidget(self.tip_label, 3, 1)
        top_layout.addWidget(self.search_content_label, 3, 0)
        top_layout.addWidget(self.search_content_text_list, 4, 0, 2, 5)

        self.setLayout(top_layout)
        self.connect(self.search_push_button, SIGNAL("clicked()"), self.search)  # 绑定点击事件

    def search(self):
        self.tip_label.setText(self.tr("正在查询请稍后..."))
        # 获取输入框文本内容
        movie_name = self.movie_name_line_edit.text()
        if movie_name:
            self.work.render(movie_name, self.movie_source_combobox, self.tip_label, self.search_content_text_list)
        else:
            self.critical("请输入搜索关键词!")


class WorkThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def render(self, movie_name, movie_source_combobox, tip_label, search_content_text_list):
        self.movies_list = []
        self.movie_source_combobox = movie_source_combobox
        self.movie_name = movie_name
        self.tip_label = tip_label
        self.search_content_text_list = search_content_text_list
        self.start()

    def get_select_movie_source(self, movie_name):
        """根据关键词请求数据"""
        # 实例化爬虫对象
        movies = SearchNews(movie_name)
        # 获取渠道文本
        select_source = self.movie_source_combobox.currentText()
        if select_source == self.tr('百度新闻'):
            data = movies.baidu_news()
        elif select_source == self.tr('新浪新闻'):
            data = movies.sina_news()
        elif select_source == self.tr('新华网'):
            data = movies.xinhua_news()
        else:
            data = None

        return data

    def run(self):
        self.movies_list = self.get_select_movie_source(self.movie_name)  # 获取数据

        self.search_content_text_list.clear()
        self.search_content_text_list.addItems(self.movie_name)
        self.tip_label.setText(self.tr("查询结束"))



        # try:
        #     self.movies_list = search_movies.get_display_content(url, params)
        # except Exception as e:
        #     print(e)
        #     self.movies_list.append(self.tr("过于频繁的访问"))
        # finally:
        #     self.search_content_text_list.clear()

app = QApplication(sys.argv)
dialog = LayoutDialog()
dialog.show()
app.exec_()
