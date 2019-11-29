import requests
import time
import hashlib
import uuid
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')


def get_sign(s):
    h = hashlib.sha256()
    h.update(s.encode('utf-8'))
    return h.hexdigest()


def get_input_str(q):
    if len(q) <= 20:
        return q
    else:
        q[:10] + len(q) + q[-10:]


def translate(q):
    """有道云文本翻译
    http://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html

    Arguments:
        q {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    curtime = str(int(time.time()))
    salt = str(uuid.uuid4())
    input_str = get_input_str(q)
    sign = get_sign(APP_ID+input_str+salt+curtime+APP_SECRET)
    # print('sign: ', sign)
    data = {
        'q': q,
        'from': 'zh-CHS',
        'to': 'en',
        'appKey': APP_ID,
        'salt': salt,
        'sign': sign,
        'signType': 'v3',
        'curtime': curtime,
    }
    res = requests.post(YOUDAO_URL, data=data)
    return res.json()


if __name__ == '__main__':
    word = input('请输入你要翻译的文字：')
    output = translate(word)
    print(output['translation'][0] or '无结果')
