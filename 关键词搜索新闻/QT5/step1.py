import requests
from bs4 import BeautifulSoup


def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('状态码返回错误，请求失败')
            return None
    except Exception as e:
        print(e)
        return None


def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')

    img_list = [s.get('data-src') for s in soup.select('dd img.board-img')]
    name_list = [s.text for s in soup.select('p.name > a')]
    star_list = [s.text.strip().split('：')[-1] for s in soup.select('p.star')]
    time_list = [s.text.strip().split('：')[-1] for s in soup.select('p.releasetime')]
    score_list = [s.text for s in soup.select('p.score')]

    for i in range(10):
        print('图片链接：{}'.format(img_list[i]))
        print('电影名称：{}'.format(name_list[i]))
        print('主演人员：{}'.format(star_list[i]))
        print('上映时间：{}'.format(time_list[i]))
        print('电影评分：{}'.format(score_list[i]))
        print('')


def main():
    base_url = 'https://maoyan.com/board/4?offset={}'
    for i in range(10):
        print('开始爬取第{}页'.format(i+1))
        url = base_url.format(i*10)
        html = get_page(url)
        parse_page(html)

    print('全部爬取完毕！')


if __name__ == '__main__':
    main()