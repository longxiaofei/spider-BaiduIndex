from qdata.baidu_search import get_all_search


def test_all_search():
    _keyword = '大碗面'
    _domain = 'dianping.com'
    _cookies = '这里放cookie'
    for result in get_all_search(keyword=_keyword, cookies=_cookies, domain=_domain):
        print(result)


if __name__ == "__main__":
    test_all_search()
