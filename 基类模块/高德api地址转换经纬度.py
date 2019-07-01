"""
利用高德地图api实现地址和经纬度的转换
"""
import requests


def geocode(address):
    parameters = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    print(address + "的经纬度：", answer['geocodes'][0]['location'])


if __name__=='__main__':
    while True:
        address = input("请输入地址:")
        # address = '北京市海淀区'
        geocode(address)
        if address == 'q':
            break