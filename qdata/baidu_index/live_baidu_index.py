from typing import List, Dict
import datetime

from . import common
from qdata.errors import QdataError, ErrorCode

ALL_KIND = ['_all', '_pc', '_wise']


def get_live_search_index(
    *,
    keywords_list: List[List[str]],
    cookies: str,
    area: int = 0
):
    if len(keywords_list) > 5:
        raise QdataError(ErrorCode.KEYWORD_LIMITED)
    encrypt_json = common.get_encrypt_json(
        start_date='',
        end_date='',
        keywords=keywords_list,
        type='live',
        area=area,
        cookies=cookies,
    )
    encrypt_datas = encrypt_json['data']['result']
    uniqid = encrypt_json['data']['uniqid']
    key = common.get_key(uniqid, cookies)
    for encrypt_data in encrypt_datas:
        keyword = [keyword_info['name'] for keyword_info in encrypt_data['key']]
        if area != 0:
            encrypt_data = encrypt_data['index'][str(area)]
        else:
            encrypt_data = encrypt_data['index'][0]
        for kind in ALL_KIND:
            encrypt_data[kind] = common.decrypt_func(key, encrypt_data[kind])
        for formated_data in format_data(encrypt_data, keyword):
            yield formated_data


def format_data(data: Dict, keyword: List[str]):
    """
        格式化堆在一起的数据
    """
    start_date, end_date = data['period'].split('|')
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    date_list = []
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += datetime.timedelta(hours=1)

    for kind in ALL_KIND:
        index_datas = data[kind]
        for i, cur_date in enumerate(date_list):
            try:
                index_data = index_datas[i]
            except IndexError:
                index_data = ''
            formated_data = {
                'keyword': keyword,
                'type': kind.lstrip('_'),
                'date': cur_date.strftime('%Y-%m-%d %H:%M:%S'),
                'index': index_data if index_data else '0'
            }
            yield formated_data
