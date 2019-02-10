from config import COOKIES, PROVINCE_CODE, CITY_CODE
from urllib.parse import urlencode
from collections import defaultdict
import datetime
import requests
import json

headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}


class BaiduIndex:
    """
        百度搜索指数
        :keywords; list or string '<keyword>,<keyword>'
        :start_date; string '2018-10-02'
        :end_date; string '2018-10-02'
        :area; int, search by cls.province_code/cls.city_code
    """

    province_code = PROVINCE_CODE
    city_code = CITY_CODE

    def __init__(self, keywords, start_date, end_date, area=0):
        """
        """
        self._keywords = keywords if isinstance(keywords, list) else keywords.split(',')
        self._time_range_list = self.get_time_range_list(start_date, end_date)
        self._all_kind = ['all', 'pc', 'wise']
        self._area = area
        self.result = {keyword: defaultdict(list) for keyword in self._keywords}
        self.get_result()

    def get_result(self):
        """
        """
        for start_date, end_date in self._time_range_list:
            encrypt_datas, uniqid = self.get_encrypt_datas(start_date, end_date)
            key = self.get_key(uniqid)
            for encrypt_data in encrypt_datas:
                for kind in self._all_kind:
                    encrypt_data[kind]['data'] = self.decrypt_func(key, encrypt_data[kind]['data'])
                self.format_data(encrypt_data)

    def get_encrypt_datas(self, start_date, end_date):
        """
        :start_date; str, 2018-10-01
        :end_date; str, 2018-10-01
        """
        request_args = {
            'word': ','.join(self._keywords),
            'startDate': start_date,
            'endDate': end_date,
            'area': self._area,
        }
        url = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
        html = self.http_get(url)
        datas = json.loads(html)
        uniqid = datas['data']['uniqid']
        encrypt_datas = []
        for single_data in datas['data']['userIndexes']:
            encrypt_datas.append(single_data)
        return (encrypt_datas, uniqid)

    def get_key(self, uniqid):
        """
        """
        url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
        html = self.http_get(url)
        datas = json.loads(html)
        key = datas['data']
        return key

    def format_data(self, data):
        """
        """
        keyword = str(data['word'])
        time_len = len(data['all']['data'])
        start_date = data['all']['startDate']
        cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        for i in range(time_len):
            for kind in self._all_kind:
                index_datas = data[kind]['data']
                index_data = index_datas[i] if len(index_datas) != 1 else index_datas[0]
                formated_data = {
                    'date': cur_date.strftime('%Y-%m-%d'),
                    'index': index_data if index_data else '0'
                }
                self.result[keyword][kind].append(formated_data)

            cur_date += datetime.timedelta(days=1)

    def __call__(self, keyword, kind='all'):
        return self.result[keyword][kind]

    @staticmethod
    def http_get(url, cookies=COOKIES):
        headers['Cookie'] = cookies
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    @staticmethod
    def get_time_range_list(startdate, enddate):
        """
        max 6 months
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            tempdate = startdate + datetime.timedelta(days=300)
            if tempdate > enddate:
                all_days = (enddate-startdate).days
                date_range_list.append((startdate, enddate))
                return date_range_list
            date_range_list.append((startdate, tempdate))
            startdate = tempdate + datetime.timedelta(days=1)

    @staticmethod
    def decrypt_func(key, data):
        """
        decrypt data
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

if __name__ == '__main__':
    pass
