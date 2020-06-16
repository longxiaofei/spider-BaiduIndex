from baidu_index.utils import test_cookies
from baidu_index import config
from baidu_index import BaiduIndex, ExtendedBaiduIndex

cookies = """这里放cookie"""

if __name__ == "__main__":
    # 测试cookies是否配置正确
    # True为配置成功，False为配置不成功
    print(test_cookies(cookies))

    keywords = ['爬虫', 'lol', '张艺兴', '人工智能', '华为', '武林外传']

    # 获取城市代码, 将代码传入area可以获取不同城市的指数, 不传则为全国
    # 媒体指数不能分地区获取
    print(config.PROVINCE_CODE)
    print(config.CITY_CODE)

    # 获取百度搜索指数(地区为山东)
    baidu_index = BaiduIndex(
        keywords=keywords,
        start_date='2018-01-01',
        end_date='2019-01-01',
        cookies=cookies,
        area=901
    )
    for index in baidu_index.get_index():
        print(index)
    

    # 获取百度媒体指数
    news_index = ExtendedBaiduIndex(
        keywords=keywords,
        start_date='2018-01-01',
        end_date='2019-01-01',
        cookies=cookies,
        kind='news'
    )
    for index in news_index.get_index():
        print(index)

    # 获取百度咨询指数
    feed_index = ExtendedBaiduIndex(
        keywords=keywords,
        start_date='2018-01-01',
        end_date='2019-01-01',
        cookies=cookies,
        kind='feed'
    )
    for index in feed_index.get_index():
        print(index)
