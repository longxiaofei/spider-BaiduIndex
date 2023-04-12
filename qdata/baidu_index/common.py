from typing import List, Dict, Tuple
from urllib.parse import urlencode, quote
from base64 import b64encode
import math
import datetime
import json

from Crypto.Cipher import AES
from qdata.errors import ErrorCode, QdataError

import requests


# pylint: disable=line-too-long
headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
}
# pylint: enable=line-too-long


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


def get_cipher_text(keyword: str) -> str:
    byte_list = [
        b"\x00", b"\x01", b"\x02", b"\x03", b"\x04", b"\x05", b"\x06", b"\x07",
        b"\x08", b"\x09", b"\x0a", b"\x0b", b"\x0c", b"\x0d", b"\x0e", b"\x0f",
        b"\x10"
    ]
    # 这个数是从acs-2057.js里写死的，但这个脚本请求时代时间戳，不确定是不是一个动态变化的脚本
    start_time = 1652338834776
    end_time = int(datetime.datetime.now().timestamp()*1000)

    wait_encrypted_data = {
        "ua": headers["User-Agent"],
        "url": quote(f"https://index.baidu.com/v2/main/index.html#/trend/{keyword}?words={keyword}"),
        "platform": "MacIntel",
        "clientTs": end_time,
        "version": "2.1.0"
    }
    password = b"yyqmyasygcwaiyaa"
    iv = b"1234567887654321"
    aes = AES.new(password, AES.MODE_CBC, iv)
    wait_encrypted_str = json.dumps(wait_encrypted_data).encode()
    filled_count = 16 - len(wait_encrypted_str) % 16
    wait_encrypted_str += byte_list[filled_count] * filled_count
    encrypted_str = aes.encrypt(wait_encrypted_str)
    cipher_text = f"{start_time}_{end_time}_{b64encode(encrypted_str).decode()}"
    return cipher_text


def split_keywords(keywords: List) -> List[List[str]]:
    """
    一个请求最多传入5个关键词, 所以需要对关键词进行切分
    """
    return [keywords[i*5: (i+1)*5] for i in range(math.ceil(len(keywords)/5))]


def http_get(url: str, cookies: str, cipher_text: str = "") -> str:
    """
        发送get请求, 程序中所有的get都是调这个方法
        如果想使用多cookies抓取, 和请求重试功能
        在这自己添加
    """
    cur_headers = headers.copy()
    cur_headers['Cookie'] = cookies
    if cipher_text:
        cur_headers["Cipher-Text"] = cipher_text
    try:
        response = requests.get(url, headers=cur_headers, timeout=30)
    except requests.Timeout as exc:
        raise QdataError(ErrorCode.NETWORK_ERROR) from exc
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
    cipher_text = get_cipher_text(keywords[0][0])
    html = http_get(url, cookies, cipher_text=cipher_text)
    datas = json.loads(html)
    if datas['status'] == 10000:
        raise QdataError(ErrorCode.NO_LOGIN)
    if datas["status"] == 10001:
        raise QdataError(ErrorCode.REQUEST_LIMITED)
    if datas['status'] != 0:
        raise QdataError(ErrorCode.UNKNOWN, str(datas))
    return datas


def test_cookies(cookies: str) -> bool:
    """
        测试cookie是否可用
    """
    html = http_get('https://www.baidu.com/', cookies)
    return '退出' in html


def check_keywords_exists(keywords: List[str], cookies: str) -> Dict[str, List[str]]:
    if len(keywords) > 15:
        raise QdataError(ErrorCode.CHECK_KEYWORD_LIMITED)

    new_keywords = []
    for i in range(0, len(keywords), 3):
        new_keyword = "+".join(keywords[i: i+3])
        new_keywords.append(new_keyword)

    base_url = "https://index.baidu.com/api/AddWordApi/checkWordsExists?"
    params = {
        "word": ",".join(new_keywords)
    }
    url = base_url + urlencode(params)
    json_data = json.loads(http_get(url, cookies))
    if json_data["status"] != 0:
        raise QdataError(ErrorCode.UNKNOWN, json_data.get("message", ""))

    not_exists_keywords = []
    for item in json_data["data"]["result"]:
        if item["status"] == 10003:
            not_exists_keywords.extend(item["word"].split(","))

    exists_keywords = [keyword for keyword in keywords if keyword not in set(not_exists_keywords)]

    return {
        "not_exists_keywords": not_exists_keywords,
        "exists_keywords": exists_keywords
    }
