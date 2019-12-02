import requests
from lxml import etree
from urllib.parse import urlsplit


def get_channel_urls(url, headers):
    print('get channel urls...')
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    channel_items = selector.xpath(
        '//div[@id="ymenu-side"]//li[@class="ym-tab"]')
    channel_urls = []
    split_url = urlsplit(url)
    base_url = split_url.scheme + '://' + split_url.netloc
    for item in channel_items:
        urls = item.xpath('span[@class="dlb"]/a/@href')
        for url in urls:
            channel_urls.append(base_url + url)
    return channel_urls
