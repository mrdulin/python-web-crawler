from src.zhuanzhuan.channel_urls_extract import get_channel_urls
from src.zhuanzhuan.db import connect_database

from lxml import etree
import requests
import time
from multiprocessing.pool import Pool
from functools import partial


base_url = 'https://tianshui.58.com'
sale_url = base_url + '/sale.shtml'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Connection': 'keep-alive'
}


def get_item_urls(channel, pn, url_collection):
    page_url = '{channel}pn{pn}/'.format(channel=channel, pn=pn)
    print('page_url: ', page_url)
    res = requests.get(page_url, headers=headers)
    selector = etree.HTML(res.text)
    infos = selector.xpath('//div[@id="infolist"]//tr')
    if infos:
        for info in infos:
            url = info.xpath('td[2]/div/a/@href')
            if url:
                url_collection.insert_one(
                    {'item_url': url[0], 'page_url': page_url})
            else:
                pass
    else:
        pass


def get_item_info(url):
    db = connect_database()
    item_info_collection = db.get_collection('zhuanzhuan_item_info')
    res = requests.get(url, headers)
    selector = etree.HTML(res.text)
    try:

        title = selector.xpath('//h1[@class="detail-title__name"]/text()')[0]
        price = selector.xpath(
            '//span[@class="infocard__container__item__main__text--price"]/text()')[0]
        area_1 = selector.xpath(
            '//div[@class="infocard__container__item__main"]/a[1]/text()')[0]
        area_2 = selector.xpath(
            '//div[@class="infocard__container__item__main"]/a[2]/text()')[0]
        view = selector.xpath(
            '//span[@class="detail-title__info__totalcount"]/text()')[0]
        info = {
            'title': title.strip(),
            'price': price.strip(),
            'area': area_1.strip() + ' - ' + area_2.strip(),
            'view': view,
            'url': url,
        }
        print(info)
        item_info_collection.insert_one(info)
    except IndexError as e:
        print(e, ', url: ', url)


def get_all_links_from(channel):
    db = connect_database()
    url_collection = db.get_collection('zhuanzhuan_url')
    print('get all links from channel: {}'.format(channel))
    for num in range(1, 10):
        get_item_urls(channel, num, url_collection)
        time.sleep(2)


def main():
    channel_urls = get_channel_urls(sale_url, headers)
    pool = Pool(processes=4)
    # pool.map(get_all_links_from, channel_urls)

    db = connect_database()
    url_collection = db.get_collection('zhuanzhuan_url')
    zhuanzhuan_item_urls = [item['item_url'] for item in url_collection.find()]
    zhuanzhuan_item_infos_urls = [item['url']
                                  for item in db.zhuanzhuan_item_info.find()]

    x = set(zhuanzhuan_item_urls)
    y = set(zhuanzhuan_item_infos_urls)
    rest_urls = x - y
    pool.map(get_item_info, rest_urls)


if __name__ == '__main__':
    main()
