import re
import csv
import time
import random
import pandas as pd
import asyncio
from retrying import retry      # 设置重试次数用的
from pyppeteer import launch
from urllib.parse import quote


width, height = 1366, 768

count = 0


async def login():
    """
    登录
    :return:
    """
    # headless=False 有头模式 dumpio=True 浏览器不会卡住
    browser = await launch({'headless': False, 'args': ['--no-sandbox'], 'dumpio': True})
    # 启动个新的浏览器页面
    page = await browser.newPage()
    # 是否启用JS，enabled设为False，则无渲染效果
    await page.setJavaScriptEnabled(enabled=True)
    # 设置浏览器尺寸
    await page.setViewport({'width': width, 'height': height})
    # 请求头
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36')

    # 打开路由
    await page.goto('https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/', {'timeout': 10000*20})
    # 由于重新跳转了页面，window.navigator.webdriver的值被改为了True，需要再次设置为undefined，否则翻页过程中出现滑块，则会一直滑动失败
    await page_evaluate(page)
    # 防止被检测selenium 此项必须设置在打开网页之前#
    # await page.evaluate(
    #     '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    input('登录')
    await asyncio.sleep(1)
    for words in read_xls():
        url = f'https://s.taobao.com/search?q={quote(words)}&sort=price-asc'
        print(url)
        await page.goto(url, {'timeout': 10000*20})
        # 由于重新跳转了页面，window.navigator.webdriver的值被改为了True，需要再次设置为undefined，否则翻页过程中出现滑块，则会一直滑动失败
        await page_evaluate(page)
        await asyncio.sleep(3)

        # 获取网页源码
        # await asyncio.sleep(1000)
        html = await page.content()
        # 是否有滑块
        while True:
            if '亲，小二正忙，滑动一下马上回来' in html:
                input('滑动')
                # print('滑动')
                # await mouse_slide(page)
                await asyncio.sleep(3)
                html = await page.content()
                await page_evaluate(page)
                continue
            break
        commodity_id = re.findall(r'data-nid="(.*?)"', html, re.S | re.M)
        await asyncio.sleep(5)
        commodity_url = f'https://item.taobao.com/item.htm?ft=t&id={commodity_id[0]}'
        print(commodity_url)
        await page.goto(commodity_url, {'timeout': 10000*20})
        # 由于重新跳转了页面，window.navigator.webdriver的值被改为了True，需要再次设置为undefined，否则翻页过程中出现滑块，则会一直滑动失败
        await page_evaluate(page)
        # 店铺
        shop = await page.xpath('//*[@id="J_ShopInfo"]/div/div[1]/div[1]/dl/dd/strong/a')
        shop = await (await shop[0].getProperty("title")).jsonValue()  # 提取对象文本值
        print(shop)
        # 金额
        money = await page.xpath('//*[@id="J_StrPrice"]/em[2]')
        print(money)
        money = await (await money[0].getProperty("textContent")).jsonValue()  # 提取对象文本值
        print(money)
        if '-' in money:
            money = money.split('-')[0]
        print(money)
        # 标题
        title = await page.xpath('//*[@id="J_Title"]/h3')
        print(title)
        title = await (await title[0].getProperty("textContent")).jsonValue()  # 提取对象文本值
        title = title.strip()
        print(title)
        # 抓取时间
        writertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f'牌名:{words} 店名:{shop} 最低价:{money} 分类:{title} 时间:{writertime}')
        global count
        count += 1
        model_csv([[words, shop, money, title, writertime]])
        time.sleep(5)
        if not count % 10:
            print("程序等待60秒后继续运行：防止操作太快出错")
            time.sleep(10)


async def page_evaluate(page):
    # 替换淘宝在检测浏览时采集的一些参数。
    # 就是在浏览器运行的时候，始终让window.navigator.webdriver=false
    # navigator是windiw对象的一个属性，同时修改plugins，languages，navigator
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none,)
async def mouse_slide(page=None):
    await asyncio.sleep(3)
    print(1)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1_n1z')
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
        print(2)
    except Exception as e:
        print(e, ':验证失败')


def read_xls():
    """
    读取 XLS表格数据
    :return:
    """
    # 加载数据
    df_read = pd.read_excel('config/查询记录.xlsx')
    df = pd.DataFrame(df_read)
    # 获取指定表头的列数
    content = 0  # 数据列
    for i in range(len(df.keys())):
        if df.keys()[i] == '牌名':
            content = i
    for indexs in df.index:
        # 获取企业信息 查询用
        pre_name = df.ix[indexs, content]
        print(pre_name)
        yield (pre_name)


def model_csv(data):
    """保存数据"""
    with open("demo.csv", "a+", encoding='GBK', newline="") as f:
        k = csv.writer(f, delimiter=',')
        with open("demo.csv", "r", encoding='GBK', newline="") as f1:
            reader = csv.reader(f1)
            if not [row for row in reader]:
                k.writerow(['牌名', '店名', '最低价', '分类', '抓取时间'])
                k.writerows(data)
                print('第[{}]条数据插入成功'.format(count))
            else:
                k.writerows(data)
                print('第[{}]条数据插入成功'.format(count))


async def run():
    await login()


if __name__ == '__main__':
    # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    loop = asyncio.get_event_loop()
    # 将协程注册到事件循环，并启动事件循环
    loop.run_until_complete(run())


"""
常见错误：
1、pyppeteer.errors.NetworkError: Protocol Error (Runtime.callFunctionOn): Session closed. Most likely the page has been closed.
    解决方法：https://github.com/miyakogi/pyppeteer/pull/160/files
"""