# -*- coding:utf-8 -*-
# 文件 ：全系车型参数(包含历史车型).py
# IED ：PyCharm
# 时间 ：2019/12/13 0013 14:48
# 版本 ：V1.0
import os
import re
import bs4
import json
import xlwt
import requests
from lxml import etree
from selenium import webdriver


class Spider:
    def __init__(self):
        pass

    def get_car_parser(self):
        """解析汽车之家所有车系数据保存"""
        # 构造A-Z列表 不加1只到Y
        letters = [chr(i) for i in range(ord('A'), ord('Z')+1)]
        print(letters)
        for letter in letters:
            if letter is None:
                continue
            # 品牌拼音首字母页面
            Brand_url = f'https://www.autohome.com.cn/grade/carhtml/{letter}.html'
            print(f'{letter} {Brand_url}')
            # 开始获取每个品牌的车型
            Brand_resp = requests.get(Brand_url, timeout=30)
            # 获取品牌车型网页源码
            Brand_html = bs4.BeautifulSoup(str(Brand_resp.content, "gbk"), "html.parser")
            # 提取网页中所有li标签
            li_labels = Brand_html.find_all("li")

            for li_label in li_labels:
                # 提取li标签下的h4标签
                h4_label = li_label.h4
                if h4_label is None:
                    continue
                # 提取h4标签下a标签href属性值
                href = str(h4_label.a.attrs['href'])
                # 提取车型ID
                model_id = href.split("#")[0]
                model_id = model_id[model_id.index(".cn")+3:].replace("/", '')
                print(model_id)
                if model_id is None:
                    continue
                # 获取停售车型参数页面url
                model_urls = self.get_discontinued_models(model_id)
                car_url = f'https://car.autohome.com.cn/config/series/{model_id}.html'
                model_urls.append(car_url)
                for model_url in model_urls:
                    car_file = re.findall(r'series/(.*?)\.html', model_url)[0]
                    # 存储车系参数页面源码
                    car_resp = requests.get(model_url, timeout=30)
                    text = str(car_resp.content, encoding="utf-8")
                    if '抱歉，暂无相关数据' in text:
                        print(f"model_url:{model_url} 无数据跳过!")
                        continue
                    print(f"model_url:{model_url}")
                    # 效验文件夹是否存在 不存在则创建
                    model_page = '1-车型参数页面源码'
                    if not os.path.exists(model_page):
                        os.makedirs(model_page)
                    with open(model_page + '/' + car_file, 'w', encoding='utf-8') as f:
                        f.write(text)
            return

    def get_discontinued_models(self, model_id):
        """
        提取停售车型年份ID 拼接车系参数url
        model_id ： 车系id
        :return: 车型详细参数url
        """
        model_urls = []
        url = f'https://www.autohome.com.cn/{model_id}/sale.html'
        response = requests.get(url, timeout=30)
        html = etree.HTML(response.text)
        # 停售车型ID
        years_id = html.xpath('//div[@class="title-subcnt-tab"]/ul/li/a/@data-yearid')
        # 判断是否有更多停售车型
        title = html.xpath('//div[@class="title-subcnt-tab"]/ul/li//text()')
        if '更多' in title:
            more = html.xpath('//li[@data-toggle="overlay"]/div/dl/dd/a/@data-yearid')
            titles = years_id + more
        else:
            titles = years_id
        # 根据年份ID拼接停售车型参数url
        for i in titles:
            _url = f'https://car.autohome.com.cn/config/series/{model_id}-{i}.html'
            model_urls.append(_url)
        return model_urls

    def js_saved_html(self):
        """第二步 解析出每个车型参数页面的混淆字体js拼装成一个新html"""
        print("第二步 混淆字体js拼装成html...")
        rootPath = "1-车型参数页面源码/"
        files = os.listdir(rootPath)
        for file in files:
            print(f'{file} 提取页面中class混淆字体js')
            with open(rootPath + file, 'r', encoding="utf-8") as f:
                text = f.read()

            # 解析数据的json
            alljs = ("var rules = '2';"
                     "var document = {};"
                     "function getRules(){return rules}"
                     "document.createElement = function() {"
                     "      return {"
                     "              sheet: {"
                     "                      insertRule: function(rule, i) {"
                     "                              if (rules.length == 0) {"
                     "                                      rules = rule;"
                     "                              } else {"
                     "                                      rules = rules + '#' + rule;"
                     "                              }"
                     "                      }"
                     "              }"
                     "      }"
                     "};"
                     "document.querySelectorAll = function() {"
                     "      return {};"
                     "};"
                     "document.head = {};"
                     "document.head.appendChild = function() {};"

                     "var window = {};"
                     "window.decodeURIComponent = decodeURIComponent;")
            try:
                js = re.findall('(\(function\([a-zA-Z]{2}.*?_\).*?\(document\);)', text)
                for item in js:
                    alljs = alljs + item
            except Exception as e:
                print('makejs function exception')
            # 把混淆字体js拼装成HTML
            newHtml = "<html><meta http-equiv='Content-Type' content='text/html; charset=utf-8' /><head></head><body>    <script type='text/javascript'>"
            alljs = newHtml + alljs + " document.write(rules)</script></body></html>"
            # 效验文件夹是否存在 不存在则创建
            js_html_name = '2-js拼装的HTML'
            if not os.path.exists(js_html_name):
                os.makedirs(js_html_name)
            with open(js_html_name + "/" + file + ".html", "w", encoding="utf-8") as f:
                f.write(alljs)

    def model_paremeter(self):
        """第三步 解析出每个车型的参数数据json保存到本地"""
        print("第三步 解析车型参数数据...")
        rootPath = "1-车型参数页面源码/"
        files = os.listdir(rootPath)
        for file in files:
            print(f'提取：{file}车型参数信息')
            with open(rootPath + file, 'r', encoding="utf-8") as f:
                text = f.read()

            # 解析数据的json
            jsonData = ""
            config = re.search('var config = (.*?)};', text)
            if config:
                # print(config.group(0))
                jsonData = jsonData + config.group(0)
            option = re.search('var option = (.*?)};', text)
            if option:
                # print(option.group(0))
                jsonData = jsonData + option.group(0)
            bag = re.search('var bag = (.*?)};', text)
            if bag:
                # print(bag.group(0))
                jsonData = jsonData + bag.group(0)
            color = re.search('var color = (.*?)};', text)
            if color:
                # print(color.group(0))
                jsonData = jsonData + color.group(0)
            innerColor = re.search('var innerColor =(.*?)};', text)
            if innerColor:
                # print(innerColor.group(0))
                jsonData = jsonData + innerColor.group(0)

            # 效验文件夹是否存在 不存在则创建
            model_json = '3-车型参数json'
            if not os.path.exists(model_json):
                os.makedirs(model_json)
            with open(model_json + "/" + file, "w", encoding="utf-8") as f:
                f.write(jsonData)

    def extract_text(self):
        """第四步 浏览器执行第二步生成的html文件 抓取执行结果(字体混淆) 保存到本地"""
        print('第四步 浏览器执行第二步生成的html文件 抓取执行结果(字体混淆) 保存到本地')
        lists = os.listdir("2-js拼装的HTML")
        driver = webdriver.Chrome()
        for fil in lists:
            print(f'提取：{file}class混淆属性对应字体')
            # 效验文件夹是否存在 不存在则创建
            content_file = '4-抓取HTML结果'
            if not os.path.exists(content_file):
                os.makedirs(content_file)
            file = os.path.exists(content_file + '/' + fil)
            if file:
                print('文件已经解析。。。' + str(file))
                continue
            print(fil)
            driver.get(os.getcwd() + os.sep + "2-js拼装的HTML/" + fil)
            text = driver.find_element_by_tag_name('body')
            print(text.text)

            with open(content_file + "/" + fil, "w", encoding="utf-8") as f:
                f.write(text.text)

    def replace_text(self):
        """第五步 匹配样式文件与json数据文件 生成正常的数据文件"""
        print("第五步 匹配样式文件与json数据文件 生成正常的数据文件")
        rootPath = "3-车型参数json/"
        listdir = os.listdir(rootPath)
        for json_s in listdir:
            print(f'{json_s}：混淆字体替换')
            # 读取json数据文件
            model_json = ''
            with open(rootPath + json_s, 'r', encoding="utf-8") as f:
                model_json = f.read()

            # 读取样式文件
            spansPath = "4-抓取HTML结果/" + json_s + ".html"
            with open(spansPath, "r", encoding="utf-8") as f1:
                content = f1.read()

            # 获取所有span对象
            models_span = re.findall("<span(.*?)></span>", model_json)

            for model_span in models_span:
                # 获取class属性值
                sea = re.search("'(.*?)'", model_span)
                spanContent = str(sea.group(1)) + "::before { content:(.*?)}"
                # 匹配样式值
                spanContentRe = re.search(spanContent, content)
                if spanContentRe:
                    if sea.group(1):
                        # print("匹配到的样式值=" + spanContentRe.group(1))
                        # class替换为文字
                        model_json = model_json.replace(str("<span class='" + sea.group(1) + "'></span>"),
                                                        re.search("\"(.*?)\"", spanContentRe.group(1)).group(1))

            # 效验文件夹是否存在 不存在则创建
            new_json = '5-文字替换后json'
            if not os.path.exists(new_json):
                os.makedirs(new_json)
            print(model_json)
            with open(new_json + '/' + json_s, 'w', encoding='utf-8') as f2:
                f2.write(model_json)
            print('*' * 100)

    def save_xls(self):
        """第六步 保存数据"""
        count = 1
        Header = {'车型ID': 0, '车型名称': 1, '厂商指导价(元)': 2, '厂商': 3, '级别': 4, '能源类型': 5, '环保标准': 6, '上市时间': 7,
                  '工信部纯电续航里程(km)': 8, '快充时间(小时)': 9, '慢充时间(小时)': 10, '快充电量百分比': 11, '最大功率(kW)': 12, '最大扭矩(N·m)': 13,
                  '发动机': 14, '变速箱': 15, '长*宽*高(mm)': 16, '车身结构': 17, '最高车速(km/h)': 18, '官方0-100km/h加速(s)': 19,
                  '实测0-100km/h加速(s)': 20, '实测100-0km/h制动(m)': 21, '实测续航里程(km)': 22, '工信部综合油耗(L/100km)': 23,
                  '实测油耗(L/100km)': 24, '整车质保': 25, '长度(mm)': 26, '宽度(mm)': 27, '高度(mm)': 28, '轴距(mm)': 29,
                  '前轮距(mm)': 30, '后轮距(mm)': 31, '最小离地间隙(mm)': 32, '车门数(个)': 33, '座位数(个)': 34, '油箱容积(L)': 35,
                  '行李厢容积(L)': 36, '整备质量(kg)': 37, '发动机型号': 38, '排量(mL)': 39, '排量(L)': 40, '进气形式': 41, '气缸排列形式': 42,
                  '气缸数(个)': 43, '每缸气门数(个)': 44, '压缩比': 45, '配气机构': 46, '缸径(mm)': 47, '行程(mm)': 48, '最大马力(Ps)': 49,
                  '最大功率转速(rpm)': 50, '最大扭矩转速(rpm)': 51, '发动机特有技术': 52, '燃料形式': 53, '燃油标号': 54, '供油方式': 55, '缸盖材料': 56,
                  '缸体材料': 57, '电机类型': 58, '电动机总功率(kW)': 59, '电动机总扭矩(N·m)': 60, '前电动机最大功率(kW)': 61, '前电动机最大扭矩(N·m)': 62,
                  '后电动机最大功率(kW)': 63, '后电动机最大扭矩(N·m)': 64, '系统综合功率(kW)': 65, '系统综合扭矩(N·m)': 66, '驱动电机数': 67, '电机布局': 68,
                  '电池类型': 69, '电池能量(kWh)': 70, '百公里耗电量(kWh/100km)': 71, '电池组质保': 72, '快充电量(%)': 73, '挡位个数': 74,
                  '变速箱类型': 75, '简称': 76, '驱动方式': 77, '前悬架类型': 78, '后悬架类型': 79, '助力类型': 80, '车体结构': 81, '前制动器类型': 82,
                  '后制动器类型': 83, '驻车制动类型': 84, '前轮胎规格': 85, '后轮胎规格': 86, '备胎规格': 87, '主/副驾驶座安全气囊': 88, '前/后排侧气囊': 89,
                  '前/后排头部气囊(气帘)': 90, '膝部气囊': 91, '后排安全带式气囊': 92, '后排中央安全气囊': 93, '被动行人保护': 94, '胎压监测功能': 95,
                  '零胎压继续行驶': 96, '安全带未系提醒': 97, 'ISOFIX儿童座椅接口': 98, 'ABS防抱死': 99, '制动力分配(EBD/CBC等)': 100,
                  '刹车辅助(EBA/BAS/BA等)': 101, '牵引力控制(ASR/TCS/TRC等)': 102, '车身稳定控制(ESC/ESP/DSC等)': 103, '并线辅助': 104,
                  '车道偏离预警系统': 105, '车道保持辅助系统': 106, '道路交通标识识别': 107, '主动刹车/主动安全系统': 108, '夜视系统': 109, '疲劳驾驶提示': 110,
                  '前/后驻车雷达': 111, '驾驶辅助影像': 112, '倒车车侧预警系统': 113, '巡航系统': 114, '驾驶模式切换': 115, '自动泊车入位': 116,
                  '发动机启停技术': 117, '自动驻车': 118, '上坡辅助': 119, '陡坡缓降': 120, '可变悬架功能': 121, '空气悬架': 122, '电磁感应悬架': 123,
                  '可变转向比': 124, '中央差速器锁止功能': 125, '整体主动转向系统': 126, '限滑差速器/差速锁': 127, '涉水感应系统': 128, '天窗类型': 129,
                  '运动外观套件': 130, '轮圈材质': 131, '电动吸合车门': 132, '侧滑门形式': 133, '电动后备厢': 134, '感应后备厢': 135, '电动后备厢位置记忆': 136,
                  '尾门玻璃独立开启': 137, '车顶行李架': 138, '发动机电子防盗': 139, '车内中控锁': 140, '钥匙类型': 141, '无钥匙启动系统': 142,
                  '无钥匙进入功能': 143, '主动闭合式进气格栅': 144, '远程启动功能': 145, '车侧脚踏板': 146, '电池预加热': 147, '方向盘材质': 148,
                  '方向盘位置调节': 149, '多功能方向盘': 150, '方向盘换挡': 151, '方向盘加热': 152, '方向盘记忆': 153, '行车电脑显示屏幕': 154,
                  '全液晶仪表盘': 155, '液晶仪表尺寸': 156, 'HUD抬头数字显示': 157, '内置行车记录仪': 158, '主动降噪': 159, '手机无线充电功能': 160,
                  '电动可调踏板': 161, '座椅材质': 162, '运动风格座椅': 163, '主座椅调节方式': 164, '副座椅调节方式': 165, '主/副驾驶座电动调节': 166,
                  '前排座椅功能': 167, '电动座椅记忆功能': 168, '副驾驶位后排可调节按钮': 169, '第二排座椅调节': 170, '后排座椅电动调节': 171, '后排座椅功能': 172,
                  '后排小桌板': 173, '第二排独立座椅': 174, '座椅布局': 175, '后排座椅放倒形式': 176, '后排座椅电动放倒': 177, '前/后中央扶手': 178,
                  '后排杯架': 179, '加热/制冷杯架': 180, '中控彩色液晶屏幕': 181, '中控液晶屏尺寸': 182, 'GPS导航系统': 183, '导航路况信息显示': 184,
                  '道路救援呼叫': 185, '中控液晶屏分屏显示': 186, '蓝牙/车载电话': 187, '手机互联/映射': 188, '语音识别控制系统': 189, '手势控制': 190,
                  '车联网': 191, '车载电视': 192, '后排液晶屏幕': 193, '后排控制多媒体': 194, '外接音源接口类型': 195, 'USB/Type-C接口数量': 196,
                  '车载CD/DVD': 197, '220V/230V电源': 198, '行李厢12V电源接口': 199, '扬声器品牌名称': 200, '扬声器数量': 201, '近光灯光源': 202,
                  '远光灯光源': 203, '灯光特色功能': 204, 'LED日间行车灯': 205, '自适应远近光': 206, '自动头灯': 207, '转向辅助灯': 208, '转向头灯': 209,
                  '车前雾灯': 210, '前大灯雨雾模式': 211, '大灯高度可调': 212, '大灯清洗装置': 213, '大灯延时关闭': 214, '触摸式阅读灯': 215,
                  '车内环境氛围灯': 216, '前/后电动车窗': 217, '车窗一键升降功能': 218, '车窗防夹手功能': 219, '多层隔音玻璃': 220, '外后视镜功能': 221,
                  '内后视镜功能': 222, '后风挡遮阳帘': 223, '后排侧窗遮阳帘': 224, '后排侧隐私玻璃': 225, '车内化妆镜': 226, '后雨刷': 227, '感应雨刷功能': 228,
                  '可加热喷水嘴': 229, '空调温度控制方式': 230, '后排独立空调': 231, '后座出风口': 232, '温度分区控制': 233, '车载空气净化器': 234,
                  '车内PM2.5过滤装置': 235, '负离子发生器': 236, '车内香氛装置': 237, '车载冰箱': 238, '面部识别': 239,
                  'OTA升级': 240, '四驱形式': 241, '外观颜色': 242, '内饰颜色': 243, '中央差速器结构': 244, '实测快充时间(小时)': 245,
                  '实测慢充时间(小时)': 246,
                  '电动机': 247}
        rootPath = "5-文字替换后json/"
        workbook = xlwt.Workbook(encoding='ascii')  # 创建一个文件
        worksheet = workbook.add_sheet('全系车型参数(包含历史车型)')  # 创建一个表
        files = os.listdir(rootPath)
        startRow = 0  # 开始行数
        isFlag = True  # 默认记录表头
        for file in files:
            carItem = {}
            with open(rootPath + file, 'r', encoding="utf-8") as f:
                text = f.read()
            # 解析基本参数配置参数，颜色三种参数，其他参数
            config = "var config = (.*?);"
            option = "var option = (.*?)};"
            # bag = "var bag = (.*?);"
            color = "var color = (.*?);"
            innerColor = "var innerColor =(.*?);"

            configRe = re.findall(config, text)
            optionRe = re.findall(option, text)
            # bagRe = re.findall(bag, text)
            colorRe = re.findall(color, text)
            innerColorRe = re.findall(innerColor, text)

            for a in configRe:
                config = a
            for b in optionRe:
                option = b
            # for c in bagRe:
            #     bag = c
            for d in colorRe:
                color = d
            for e in innerColorRe:
                innerColor = e

            try:
                config = json.loads(config)
                option = json.loads(option + '}')
                # bag = json.loads(bag)
                # color = json.loads(color)
                # innerColor = json.loads(innerColor)

                configItem = config['result']['paramtypeitems']  # 基本参数
                optionItem = option['result']['configtypeitems']  # 配置参数
                # colorItem = color['result']['specitems'][0]['coloritems']  # 外观颜色
                # innerColorItem = innerColor['result']['specitems'][0]['coloritems']  # 内饰颜色
            except Exception as e:
                with open("错误记录.txt", "a", encoding="utf-8") as f1:
                    f1.write(file.title() + "\n")
                print(e)
                continue

            # 解析基本参数
            for param in configItem:
                for car in param['paramitems']:
                    carItem['车型ID'] = []  # 车型ID
                    carItem[car['name']] = []
                    for ca in car['valueitems']:  # 循环车型名称列表
                        if ca['specid'] not in carItem['车型ID']:
                            carItem['车型ID'].append(ca['specid'])
                        carItem[car['name']].append(ca['value'])

            # 解析配置参数
            for config in optionItem:
                for car in config['configitems']:
                    carItem[car['name']] = []
                    for ca in car['valueitems']:
                        carItem[car['name']].append(ca['value'])

            # 解析外观颜色参数
            # carItem['外观颜色'] = []  # 外观颜色
            # for car in colorItem:
            #     carItem['外观颜色'].append(car['name'])

            # 解析内饰颜色
            # carItem['内饰颜色'] = []  # 内饰颜色
            # for car in innerColorItem:
            #     carItem['内饰颜色'].append(car['name'])

            # 写入表头 startRow行数 cols列数 co标题
            if isFlag:
                co1s = 0
                for co in Header:
                    worksheet.write(startRow, co1s, co)
                    co1s += 1
                else:
                    startRow += 1
                    isFlag = False

            # 计算起止行号
            endRowNum = startRow + len(carItem['车型名称'])  # 车辆款式记录数
            for row in range(startRow, endRowNum):
                for col in carItem:
                    context = str(carItem[col][row - startRow])
                    colNum = Header[col]  # 根据项目名称查询列数
                    if not context:
                        context = '-'
                    # 写入数据 row行 colNum列 context内容
                    worksheet.write(row, colNum, context)

                print(f'第:{count}条 [{carItem["车型ID"][0]}] 数据插入成功')
                count += 1

            else:
                startRow = endRowNum
        workbook.save('Mybook.xls')

    def run(self):
        # 第一步 下载出所有车型的网页
        self.get_car_parser()
        # 第二步 解析出每个车型参数页面的混淆字体js拼装成一个新html
        self.js_saved_html()
        # 第三步 解析出每个车型的参数数据json保存到本地
        self.model_paremeter()
        # 第四步 浏览器执行第二步生成的html文件 抓取执行结果(字体混淆) 保存到本地
        self.extract_text()
        # 第五步 匹配样式文件与json数据文件 生成正常的数据文件
        self.replace_text()
        # 第六步 读取数据文件 生成excel
        self.save_xls()


if __name__ == '__main__':
    spider = Spider()
    spider.run()