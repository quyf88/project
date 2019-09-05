a = """
文章简介：在四分五裂的國家中要如何從中殘存?跟著範道的步伐一起用求生的意志朝向未來吧!!
★ 8.00  |  作家 : 圖海 & 朴基紅  |  觀看次數 : 4,695
#繁體
"""
import os
path = 'image/' + str('123')
path_name = path + '/'  + '1.txt'
if not os.path.exists(path_name):
    print(1)