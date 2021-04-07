from typing import List, Dict, Tuple
from urllib.parse import urlencode
import math
import datetime
import json

from qdata.errors import ErrorCode, QdataError

import requests


headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
}


def get_time_range_list(startdate: str, enddate: str) -> List[Tuple[str, str]]:
    """
        切分时间段
    """
    date_range_list = []
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    while 1:
        tempdate = startdate + datetime.timedelta(days=300)
        if tempdate > enddate:
            date_range_list.append((startdate, enddate))
            break
        date_range_list.append((startdate, tempdate))
        startdate = tempdate + datetime.timedelta(days=1)
    return date_range_list


def split_keywords(keywords: List) -> List[List[str]]:
    """
    一个请求最多传入5个关键词, 所以需要对关键词进行切分
    """
    return [keywords[i*5: (i+1)*5] for i in range(math.ceil(len(keywords)/5))]


def http_get(url: str, cookies: str) -> str:
    """
        发送get请求, 程序中所有的get都是调这个方法
        如果想使用多cookies抓取, 和请求重试功能
        在这自己添加
    """
    _headers = headers.copy()
    _headers['Cookie'] = cookies
    try:
        response = requests.get(url, headers=_headers, timeout=5)
    except requests.Timeout:
        raise QdataError(ErrorCode.NETWORK_ERROR)
    if response.status_code != 200:
        raise QdataError(ErrorCode.NETWORK_ERROR)
    return response.text


def get_key(uniqid: str, cookies: str) -> str:
    url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
    html = http_get(url, cookies)
    datas = json.loads(html)
    key = datas['data']
    return key


def decrypt_func(key: str, data: str) -> List[str]:
    """
        数据解密方法
    """
    a = key
    i = data
    n = {}
    s = []
    for o in range(len(a)//2):
        n[a[o]] = a[len(a)//2 + o]
    for r in range(len(data)):
        s.append(n[i[r]])
    return ''.join(s).split(',')


def get_encrypt_json(
    *,
    start_date: str,
    end_date: str,
    keywords: List[List[str]],
    type: str,
    area: int,
    cookies: str
) -> Dict:
    pre_url_map = {
        'search': 'http://index.baidu.com/api/SearchApi/index?',
        'live': 'http://index.baidu.com/api/LiveApi/getLive?',
        'news': 'http://index.baidu.com/api/NewsApi/getNewsIndex?',
        'feed': 'http://index.baidu.com/api/FeedSearchApi/getFeedIndex?'
    }

    pre_url = pre_url_map[type]
    word_list = [
        [{'name': keyword, 'wordType': 1} for keyword in keyword_list]
        for keyword_list in keywords
    ]
    if type == 'live':
        request_args = {
            'word': json.dumps(word_list),
            'region': area
        }
    else:
        request_args = {
            'word': json.dumps(word_list),
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'area': area
        }
    url = pre_url + urlencode(request_args)
    html = http_get(url, cookies)
    datas = json.loads(html)
    if datas['status'] == 10000:
        raise QdataError(ErrorCode.NO_LOGIN)
    if datas['status'] != 0:
        raise QdataError(ErrorCode.UNKNOWN)
    return datas


def test_cookies(cookies: str) -> bool:
    """
        测试cookie是否可用
    """
    html = http_get('https://www.baidu.com/', cookies)
    return '退出' in html
