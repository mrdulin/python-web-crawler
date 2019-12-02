import time
from multiprocessing.pool import Pool


def scraper(url):
    time.sleep(1)
    return url


def main():
    urls = []
    for i in range(0, 10):
        urls.append(i)

    start_1 = time.time()
    for url in urls:
        scraper(url)
    end_1 = time.time()
    print('串行爬虫:', end_1 - start_1)

    # start_2 = time.time()
    # pool = Pool(processes=2)
    # pool.map(scraper, urls)
    # end_2 = time.time()
    # print('两个进程：', end_2 - start_2)

    # start_2 = time.time()
    # pool = Pool(processes=4)
    # pool.map(scraper, urls)
    # end_2 = time.time()
    # print('四个进程：', end_2 - start_2)


if __name__ == '__main__':
    main()
