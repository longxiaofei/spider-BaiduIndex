# coding=utf-8
from typing import Dict, Iterator

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


def get_url(url: str) -> str:
    """extract special url"""
    try:
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 302 and 'Location' in r.headers.keys():
            return r.headers['Location']
    except Exception:
        pass
    return ''


def get_search(*, keyword: str, pn: int, cookies: str, domain: str = None) -> Iterator[Dict]:
    keyword = 'site: {} {}'.format(domain, keyword) if domain else keyword
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
    response = requests.get('https://www.baidu.com/s', headers=headers, params=params)
    html = etree.HTML(response.text)
    items = html.xpath('//*/h3/a')
    for item in items:
        title = ''.join(item.xpath('.//text()'))
        href = item.xpath('./@href')[0]
        url = get_url(href)
        if not url:
            continue
        if domain and domain not in url:
            continue
        yield {'title': title, 'url': url}


def get_all_search(*, keyword: str, cookies: str, domain: str = None) -> Iterator[Dict]:
    for pn in range(1, 76):
        for item in get_search(
            keyword=keyword,
            pn=pn,
            cookies=compile,
            domain=domain
        ):
            yield item
