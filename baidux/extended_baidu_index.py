from urllib.parse import urlencode
import queue
import datetime
import json

import requests

from . import utils


class ExtendedBaiduIndex:
    """
        百度搜索指数(获取咨询指数或者媒体指数)
        :keywords; list
        :start_date; string '2018-10-02'
        :end_date; string '2018-10-02'
        :type; string 'news'(媒体) or 'feed'(咨询)
        :area; int, search by cls.province_code/cls.city_code
    """
    pre_url_dict = {
        'news': 'http://index.baidu.com/api/NewsApi/getNewsIndex?',
        'feed': 'http://index.baidu.com/api/FeedSearchApi/getFeedIndex?'
    }

    def __init__(
        self,
        *, 
        keywords: list,
        start_date: str,
        end_date: str,
        cookies: str,
        kind="news",
        area=0
    ):
        self.kind = kind
        self.keywords = keywords
        self.area = area
        self.start_date = start_date
        self.end_date = end_date
        self.cookies = cookies
        self._pre_url = self.pre_url_dict[kind]
        self._params_queue = utils.get_params_queue(start_date, end_date, keywords)

    def get_index(self):
        """
        获取百度指数
        返回的数据格式为:
        {
            'keyword': '武林外传',
            'type': 'wise',
            'date': '2019-04-30',
            'index': '202'
        }
        """
        while 1:
            try:
                params_data = self._params_queue.get(timeout=1)
                encrypt_datas, uniqid = self._get_encrypt_datas(
                    start_date=params_data['start_date'],
                    end_date=params_data['end_date'],
                    keywords=params_data['keywords']
                )
                key = utils.get_key(uniqid, self.cookies)
                for encrypt_data in encrypt_datas:
                    encrypt_data['data'] = utils.decrypt_func(key, encrypt_data['data'])
                    for formated_data in self._format_data(encrypt_data):
                        yield formated_data
            except requests.Timeout:
                self._params_queue.put(params_data)
            except queue.Empty:
                break
            utils.sleep_func()

    def _get_encrypt_datas(self, start_date, end_date, keywords):
        """
        :start_date; str, 2018-10-01
        :end_date; str, 2018-10-01
        :keyword; list, ['1', '2', '3']
        """
        word_list = [
            [{'name': keyword, 'wordType': 1} for keyword in keyword_list]
            for keyword_list in keywords
        ]
        request_args = {
            'word': json.dumps(word_list),
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'area': self.area
        }
        url = self._pre_url + urlencode(request_args)
        html = utils.http_get(url, self.cookies)
        datas = json.loads(html)
        uniqid = datas['data']['uniqid']
        encrypt_datas = []
        for single_data in datas['data']['index']:
            encrypt_datas.append(single_data)
        return (encrypt_datas, uniqid)

    def _format_data(self, data):
        """
            格式化堆在一起的数据
        """
        keyword = str(data['key'])
        start_date = datetime.datetime.strptime(data['startDate'], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(data['endDate'], '%Y-%m-%d')
        date_list = []
        while start_date <= end_date:
            date_list.append(start_date)
            start_date += datetime.timedelta(days=1)

        index_datas = data['data']
        for i, cur_date in enumerate(date_list):
            try:
                index_data = index_datas[i]
            except IndexError:
                index_data = ''
            formated_data = {
                'keyword': [keyword_info['name'] for keyword_info in json.loads(keyword.replace('\'', '"'))],
                'date': cur_date.strftime('%Y-%m-%d'),
                'index': index_data if index_data else '0'
            }
            yield formated_data
