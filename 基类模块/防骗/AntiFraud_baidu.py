import os
from aip import AipSpeech


# ----------------------------------
# 调用百度AI API
# 如果有不付尾款的就在百度AI后台把应用删掉
# ----------------------------------


def aipspeech():
    """ 18210836362 你的 APPID AK SK """
    APP_ID = '15434389'
    API_KEY = 'LwmLHenAnw8ku15M75XCmQBq'
    SECRET_KEY = 'RdNdVyolT8XZ1wtEA2SZO59REDhodpcc'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    try:
        # 合成
        result = client.synthesis('死骗子快点给钱', 'zh', 1, {
            'vol': 5,
        })

        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            return True
            # with open('auido.mp3', 'wb') as f:
            #     f.write(result)
        else:
            print('程序运行错误,联系开发者!!!')
            os._exit(0)
    except:
        print('程序运行错误,联系开发者!!!')
        os._exit(0)


if __name__ == '__main__':
    aipspeech()