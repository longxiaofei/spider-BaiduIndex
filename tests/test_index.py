from baidu_index import BaiduIndex

cookies = """xxx"""
keywords = [['百度', '搜狗']]

bd = BaiduIndex(
    keywords=keywords,
    start_date='2020-01-01',
    end_date='2021-01-01',
    cookies=cookies
)
for index in bd.get_index():
    print(index)
