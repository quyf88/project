import requests
from lxml import etree


def downLoadImage(fileName, downLoadUrl):
    r = requests.get(downLoadUrl)
    fileName = fileName + ".png"
    print("正在下载 " + fileName)
    with open("img/" + fileName, 'wb') as f:
        f.write(r.content)


response = requests.get("https://car.m.autohome.com.cn/")
response.encoding = 'UTF-8'
html = etree.HTML(response.text)
items = html.xpath('//*[@class="item"]')
for item in items:
    logo_url = item.xpath('./img/@data-src')
    if not logo_url:
        continue
    text = item.xpath('./span')[0].text
    downLoadImage(text, logo_url[0])


