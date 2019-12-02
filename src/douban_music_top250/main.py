

import os
import time
import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
import pymongo
from dotenv import load_dotenv


load_dotenv(verbose=True)

MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
dir_path = os.path.dirname(os.path.realpath(__file__))
fileName = dir_path + '/douban_music_top250.csv'


def get_music_detail(url):
    res = requests.get(url, headers=headers)
    decoded_content = res.content.decode('utf-8')
    selector = etree.HTML(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    music_name = re.findall(
        '<h1>.*?<span>(.*?)</span>', decoded_content, re.S)[0]
    music_author = re.findall('表演者:.*?>(.*?)</a>', decoded_content, re.S)[0]
    # TODO: change selector
    music_style = soup.select_one(
        '#info > span:nth-child(3)')
    music_publish_time = soup.select_one(
        '#info > span:nth-child(9)')
    music_publisher = soup.select_one(
        '#info > span:nth-child(11)')
    music_score = re.findall(
        '<strong class="ll rating_num" property="v:average">(.*?)</strong>', decoded_content, re.S)[0]

    if music_publish_time:
        music_publish_time = music_publish_time.next_sibling.strip()
    if music_publisher:
        music_publisher = music_publisher.next_sibling.strip()

    if not music_publisher:
        music_publisher = '未知'
    if not music_style:
        music_style = '未知'
    else:
        music_style = music_style.next_sibling.strip()

    print('music_name: {music_name}, music_author: {music_author}, music_style: {music_style}, music_score: {music_score}, music_publish_time: {music_publish_time}'.format(
        music_name=music_name, music_author=music_author, music_style=music_style, music_score=music_score, music_publish_time=music_publish_time))

    music_info_dict = {
        'name': music_name,
        'author': music_author,
        'style': music_style,
        'publish_time': music_publish_time,
        'publisher': music_publisher,
        'score': music_score
    }
    return music_info_dict


def get_musics_by_page(url):
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    music_infos = selector.xpath(
        '//div[@class="article"]//table//tr[@class="item"]')
    music_info_dicts = []
    for music_info in music_infos:
        music_detail_link = music_info.xpath(
            'td[2]/div/a/@href')[0]
        music_info_dicts.append(get_music_detail(music_detail_link))

    return music_info_dicts


def main():
    print('MONGODB_DATABASE: ', MONGODB_DATABASE)
    print('MONGODB_USERNAME: ', MONGODB_USERNAME)
    print('MONGODB_PASSWORD: ', MONGODB_PASSWORD)
    client = pymongo.MongoClient(host='localhost', port=27017,
                                 username=MONGODB_USERNAME, password=MONGODB_PASSWORD, authSource=MONGODB_DATABASE)
    db = client.get_database(MONGODB_DATABASE)
    collection = db.get_collection('music_top250')
    urls = ['https://music.douban.com/top250?start={start}'.format(
        start=start) for start in range(0, 250, 25)]
    for url in urls:
        music_info_dicts = get_musics_by_page(url)
        collection.insert_many(music_info_dicts)
        time.sleep(2)


if __name__ == '__main__':
    main()
