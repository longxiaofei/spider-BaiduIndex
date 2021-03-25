from qdata.baidu_index import get_feed_index, get_news_index, get_search_index


keywords_list = [['张艺兴', '汪峰'], ['百度']]
cookies = """xxx"""


def test_get_feed_index():
    for index in get_feed_index(
        keywords_list=keywords_list,
        start_date='2018-01-01',
        end_date='2019-05-01',
        cookies=cookies
    ):
        print(index)


def test_get_news_index():
    for index in get_news_index(
        keywords_list=keywords_list,
        start_date='2018-01-01',
        end_date='2019-05-01',
        cookies=cookies
    ):
        print(index)


def test_get_search_index():
    for index in get_search_index(
        keywords_list=keywords_list,
        start_date='2018-01-01',
        end_date='2019-05-01',
        cookies=cookies
    ):
        print(index)


if __name__ == "__main__":
    test_get_feed_index()
    test_get_news_index()
    test_get_search_index()
