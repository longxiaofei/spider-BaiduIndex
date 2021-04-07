from qdata.baidu_index import (
    get_feed_index,
    get_news_index,
    get_search_index,
    get_live_search_index
)


keywords_list = [['张艺兴', '汪峰'], ['百度']]
cookies = """xxx"""


def test_get_feed_index():
    """获取资讯指数"""
    for index in get_feed_index(
        keywords_list=keywords_list,
        start_date='2018-01-01',
        end_date='2019-05-01',
        cookies=cookies
    ):
        print(index)


def test_get_news_index():
    """获取媒体指数"""
    for index in get_news_index(
        keywords_list=keywords_list,
        start_date='2018-01-01',
        end_date='2019-05-01',
        cookies=cookies
    ):
        print(index)


def test_get_search_index():
    """获取搜索指数"""
    for index in get_search_index(
        keywords_list=keywords_list,
        start_date='2018-01-01',
        end_date='2019-05-01',
        cookies=cookies
    ):
        print(index)


def test_get_live_search_index():
    """获取搜索指数实时数据"""
    for index in get_live_search_index(
        keywords_list=keywords_list,
        cookies=cookies,
        area=0
    ):
        print(index)

    for index in get_live_search_index(
        keywords_list=keywords_list,
        cookies=cookies,
        area=911
    ):
        print(index)


if __name__ == "__main__":
    test_get_feed_index()
    test_get_news_index()
    test_get_search_index()
    test_get_live_search_index()
