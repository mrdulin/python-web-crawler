import requests
from bs4 import BeautifulSoup
import time
import os
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
dir_path = os.path.dirname(os.path.realpath(__file__))
fileName = dir_path + '/data.txt'


def get_sex(class_name):
    if class_name == ['member_ico1']:
        return '女'
    return '男'


def get_detail_links(url):

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    links = soup.select('#page_list > ul > li > a')

    for link in links:
        href = link.get('href')
        # print('href: {href}'.format(href=href))
        get_detail_info(href)


def get_detail_info(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select(
        'div.pho_info > h4')
    addrs = soup.select(
        'div.pho_info > p > span')
    prices = soup.select(
        '#pricePart > div.day_l > span')
    names = soup.select(
        '#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    sexes = soup.select(
        '#floatRightBox > div.js_box.clearfix > div.member_pic > div')
    avatars = soup.select(
        '#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')

    f = open(fileName, 'a+', encoding='utf-8')
    for title, addr, price, name, sex, avatar in zip(titles, addrs, prices, names, sexes, avatars):
        data = {
            'title': title.get_text().strip(),
            'addr': addr.get_text().strip(),
            'price': price.get_text().strip(),
            'name': name.get_text().strip(),
            'sex': get_sex(sex.get('class')),
            'avatar': avatar.get('src')
        }
        print(data)
        f.write(json.dumps(data, ensure_ascii=False) + '\n')
    f.close()


if __name__ == '__main__':

    if not os.path.exists(fileName):
        open(fileName, 'w', encoding='utf-8').close()

    urls = [
        'https://sh.xiaozhu.com/zhengzu-duanzufang-p{}-0/'.format(number) for number in range(1, 14)]
    for pageNum, url in enumerate(urls, start=1):
        print('====pageNum: {pageNum}===='.format(pageNum=pageNum))
        get_detail_links(url)
        time.sleep(2)
