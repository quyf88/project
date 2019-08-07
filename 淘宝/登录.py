# -*- coding: utf-8 -*-
# @Time    : 2019/8/7 15:30
# @Author  : project
# @File    : 登录.py
# @Software: PyCharm


# -*- coding: UTF-8 -*-
import asyncio
from pyppeteer import launch
import time,random

width, height = 1366, 768#设置浏览器大小
username="#####"#账号
pwd="########"#密码
async def main():
    browser = await launch(headless=False,args=[f'--window-size={width},{height}'])#类似chrom的设置
    page = await browser.newPage()#打开浏览器
    await page.setViewport({'width': width, 'height': height})#引用大小
    await page.evaluateOnNewDocument("""
    var _navigator={};
    for (name in window.navigator) {
        if (name !="webdriver"){
            _navigator[name] = window.navigator[name]
        }
    }
    Object.defineProperties(window,: 'navigator',{
        get: () =>  _navigator,
     })
    """)#这是打开访问网页前注入的js
    #类似于mitmpoxy中间人注入js


    #https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/
    await page.goto('https://login.taobao.com/member/login.jhtml?tpl_redirect_url=https%3A%2F%2Fwww.tmall.com&style=miniall&enup=true&newMini2=true&full_redirect=true&sub=true&from=tmall&allp=assets_css%3D3.0.10/login_pc.css')#访问天猫iframe的链接
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {}, }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')       #运行程序中中可以回调的js



    await page.evaluate('''document.getElementsByClassName("J_Quick2Static")[0].click()''')#点击页面的账号密码登录
    time.sleep(1)
    # await asyncio.sleep(100)
    await page.type('.J_UserName', username, {'delay': input_time_random() - 50})#输入账号 设置输入时间
    time.sleep(1)
    await page.type('#J_StandardPwd input', pwd, {'delay': input_time_random()})#输入密码


    #如果出现滑块
    try:
        await page.hover('#nc_1_n1z')  # 不同场景的验证码模块能名字不同。
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})#设置滑块速度随机
        await page.mouse.up()
        time.sleep(1)
        await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')#点击登录按钮
        time.sleep(10000)
    except:
        #如果没有出现滑块
        await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')#点击登录按钮
        time.sleep(1000)
def input_time_random():
    return random.randint(100, 151)#生成随机时间
asyncio.get_event_loop().run_until_complete(main())#pyppeteer调用协程
