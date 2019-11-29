import requests
from lxml import etree
import time
import os
import csv


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
dir_path = os.path.dirname(os.path.realpath(__file__))
fileName = dir_path + '/douban_books_top250.csv'


def get_page_info(url, start):
    # 如果不设置UA, http status code将返回418
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    bookInfos = selector.xpath('//tr[@class="item"]')

    f = open(fileName, 'a+', newline='', encoding='utf-8')
    writer = csv.writer(f)

    for i, bookInfo in enumerate(bookInfos, 1):
        rank = start * 25 + i
        name = bookInfo.xpath('td/div/a/@title')[0]
        url = bookInfo.xpath('td/div/a/@href')[0]
        intro = bookInfo.xpath('td/p/text()')[0]
        author = intro.split('/')[0]
        publisher = intro.split('/')[-3]
        date = intro.split('/')[-2]
        price = intro.split('/')[-1]
        rate = bookInfo.xpath('td/div/span[2]/text()')[0]
        comments = bookInfo.xpath('td/p/span/text()')
        comment = comments[0] if len(comments) > 0 else ''
        writer.writerow((rank, name, url, author, publisher,
                         date, price, rate, comment))
    f.close()


def main():
    if not os.path.exists(fileName):
        f = open(fileName, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerow(
            ('rank', 'name', 'url', 'author', 'publisher', 'date', 'price', 'rate', 'comment'))
        f.close()

    urls = ['https://book.douban.com/top250?start={start}'.format(
        start=start) for start in range(0, 250, 25)]
    for start, url in enumerate(urls, 0):
        get_page_info(url, start)
        time.sleep(2)


if __name__ == '__main__':
    main()
