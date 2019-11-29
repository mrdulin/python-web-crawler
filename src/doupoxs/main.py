import requests
import re
import time
import os
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
dir_path = os.path.dirname(os.path.realpath(__file__))
fileName = dir_path + '/data.txt'


def get_chapter_content(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        decoded_content = res.content.decode('utf-8')
        soup = BeautifulSoup(decoded_content, 'html.parser')
        title = soup.select('.entry-tit > h1')[0]
        # or
        # title = re.findall(
        #     '<div class="entry-tit">.*?<h1>(.*?)</h1>', decoded_content, re.S)
        # print(title)
        contents = re.findall(
            '<p>(.*?)</p>', decoded_content, re.S)
        f = open(fileName, 'a+')
        f.write(title.get_text()+'\n')
        for content in contents:
            f.write(content+'\n')
        f.close()
    else:
        pass


def main():

    urls = ['http://www.doupoxs.com/doupocangqiong/{chapterNum}.html'.format(
        chapterNum=chapterNum) for chapterNum in range(1, 1646)]
    for url in urls:
        get_chapter_content(url)
        time.sleep(2)


if __name__ == '__main__':
    main()
