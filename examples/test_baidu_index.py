from qdata.baidu_index import (
    get_feed_index,
    get_news_index,
    get_search_index,
    get_live_search_index
)
from qdata.baidu_index.common import check_keywords_exists


keywords_list = [['张艺兴', '汪峰'], ['百度'], ['gucci','古驰']]
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


def test_check_keywords():
    test_keywords = [
        "狗狗国故", "狗狗国的", "狗狗国的的", "狗狗国解决的", "男的女的给你吧大实现",
        "对你的回复", "电脑看是否", "面对面方法的", "那地方法规股份", "的那女的",
        "英短", "CF", "新冠疫苗", "极限挑战", "大家大家都"
    ]
    result = check_keywords_exists(test_keywords, cookies)
    print(result["not_exists_keywords"])
    print(result["exists_keywords"])


if __name__ == "__main__":
    test_get_feed_index()
    test_get_news_index()
    test_get_search_index()
    test_get_live_search_index()
