"""
数据可视化
"""
import re

from yingping.maoyan.database_sql import DataBase
from pyecharts import Geo, WordCloud, GeoLines, Style
from collections import Counter


def geo_formatter(params):
    """剔除Geo图中经纬度"""
    return params.name + ' : ' + params.value[2]


def geo_drawing():
    """Geo坐标图"""
    # 读取处理数据
    cityname_sql = "select cityname from maoyan_wumingzhibei where movie_name = '无名之辈'"
    data_tuple = DataBase().create(cityname_sql)
    data_counter = Counter((i[0] for i in data_tuple))
    data = dict(data_counter)
    # 初始化配置
    # 'title_color'文本标题颜色; 'title_pos'标题位置; 'background_color'画布背景颜色
    geo = Geo("《毒液》观影人群分布图", "猫眼数据", title_color="#fff",
              title_pos="center", width=1200, height=800, background_color='#404a59')

    # 过滤无坐标数据
    for n, m in data.items():
        list_1 = []
        list_2 = []
        list_1.append(n)
        list_2.append(m)

        try:
            # 'type'动画效果; 'is_random'随机排列颜色; 'effect_scale'波动大小; 'is_more_utils'实用工具按钮
            # 'visual_range' 指定组件的允许的最小值与最大值 'is_visualmap' 是否使用视觉映射组件默认Flase
            geo.add("", list_1, list_2, type="effectScatter", tooltip_formatter=geo_formatter,
                    is_label_emphasis=False, visual_range=[0, 500], is_visualmap=True,
                    is_random=False, effect_scale=5, is_more_utils=True)
        except Exception as e:
            print(e)
            pass

    geo.show_config()
    geo.render("影评1.html")


def wordcloud():
    """词云图"""
    # 读取处理数据
    wordcloud_sql = "select content from maoyan_wumingzhibei WHERE movie_name='无名之辈'"
    wordcloud_data = DataBase().create(wordcloud_sql)
    wordcloud_list = [re.sub(r'[ /….，！。?\n]', '', "".join(i)) for i in wordcloud_data]
    data_dict = dict(Counter(wordcloud_list))
    # 生成图表
    wordcloud = WordCloud(width=1300, height=620)
    attr, value = wordcloud.cast(data_dict)
    wordcloud.add("", attr, value, word_size_range=[30, 90], is_more_utils=True)
    wordcloud.render("词云图.html")


def geolines():
    """地理坐标系线图"""
    data_beijing = [
        ["北京", "上海"],
        ["北京", "广州"],
        ["北京", "南京"],
        ["北京", "重庆"],
        ["北京", "兰州"],
        ["北京", "杭州"]
        ]
    data_guangzhou = [
        ["广州", "上海", 10],
        ["广州", "北京", 20],
        ["广州", "南京", 30],
        ["广州", "重庆", 40],
        ["广州", "兰州", 50],
        ["广州", "杭州", 60],
        ]
    data_shanghai = [
        ["上海", "广州", 10],
        ["上海", "北京", 20],
        ["上海", "南京", 30],
        ["上海", "重庆", 40],
        ["上海", "兰州", 50],
        ["上海", "杭州", 60],
    ]
    style = Style(
        title_top="#fff",
        title_pos="center",
        width=1200,
        height=800,
        background_color="#404a59"
    )
    style_geo = style.add(
        is_label_show=True,
        line_curve=0.2,
        line_opacity=0.6,
        legend_text_color="#eee",
        legend_pos="right",
        geo_effect_symbol="plane",
        geo_effect_symbolsize=15,
        label_color=['#a6c84c', '#ffa022', '#46bee9'],
        label_pos="right",
        label_formatter="{b}",
        label_text_color="#eee",
    )
    geolines = GeoLines("地理坐标系线图", **style.init_style)
    geolines.add("从广州出发", data_guangzhou, **style_geo)
    geolines.add("从北京出发", data_beijing, **style_geo)
    geolines.add("从上海出发", data_shanghai, **style_geo)
    geolines.render("地理坐标系线图.html")


if __name__ == '__main__':
    geolines()