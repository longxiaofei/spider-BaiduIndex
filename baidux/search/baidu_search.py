# coding=utf-8

import requests
from lxml import etree

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.baidu.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


class BaiduSearch(object):
    def __init__(self, keyword, cookies, domain=None):
        self.keyword = keyword
        self.domain = domain
        self.cookies = cookies

    def search(self, keyword, pn):
        params = (
            ('wd', keyword),
            ('pn', (pn - 1) * 10),
            ('oq', keyword),
            ('tn', 'baiduhome_pg'),
            ('ie', 'utf-8'),
            ('rsv_idx', '2'),
            ('rsv_pq', 'd09ea91a000533ad'),
            ('rsv_t', 'a741enhrt8jcViHd/8Q+gb0DnCzjIbctyKmpOkRk6BibYwnyQXvHFSqrZtTKeUHQlE4s'),
        )
        headers['Cookie'] = self.cookies
        response = requests.get('https://www.baidu.com/s', headers=headers, params=params)
        return response

    @classmethod
    def get_url(cls, url):
        """extract special url"""
        try:
            r = requests.get(url, allow_redirects=False)
            if r.status_code == 302 and 'Location' in r.headers.keys():
                return r.headers['Location']
        except Exception:
            pass
        return ''

    def get_search(self):
        keyword = 'site: {} {}'.format(self.domain, self.keyword) if self.domain else self.keyword
        for pn in range(1, 76):
            response = self.search(keyword, pn)
            html = etree.HTML(response.text)
            items = html.xpath('//*/h3/a')
            for item in items:
                title = ''.join(item.xpath('.//text()'))
                href = item.xpath('./@href')[0]
                url = self.get_url(href)
                if not url:
                    continue
                if self.domain and self.domain not in url:
                    continue
                yield {'title': title, 'url': url}


if __name__ == '__main__':
    _keyword = '大碗面'
    _domain = 'dianping.com'
    _cookies = '这里放cookie'
    b = BaiduSearch(_keyword, _cookies, _domain)
    for item in b.get_search():
        print(item)
