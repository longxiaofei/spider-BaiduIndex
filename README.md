# Baidux - Python SDK for index and search

* http://index.baidu.com/
* http://www.baidu.com/

### Install

```shell script
# 暂时不可用
pip install baidux 
```

### Usage

打开百度首页，登录后，找到 www.baidu.com 此条 GET 请求，并复制此条请求 request headers 里的 cookies

使用样例如下：

```python
from baidux.index import (
    get_feed_index,
    get_news_index,
    get_search_index,
    test_cookies,
    PROVINCE_CODE,
    CITY_CODE
)

cookies = """这里放cookie"""

# 测试cookies是否配置正确
# True为配置成功，False为配置不成功
print(test_cookies(cookies))

keywords = [['英雄联盟'], ['冠军杯', '英雄联盟'], ['抑郁', '自杀', '明星']]

# 获取城市代码, 将代码传入area可以获取不同城市的指数, 不传则为全国
# 媒体指数不能分地区获取
print(PROVINCE_CODE)
print(CITY_CODE)

# 获取百度搜索指数(地区为山东)
for index in get_feed_index(
    keywords_list=keywords,
    start_date='2018-01-01',
    end_date='2019-05-01',
    cookies=cookies
):
    print(index)

# 获取百度媒体指数
for index in get_news_index(
    keywords_list=keywords_list,
    start_date='2018-01-01',
    end_date='2019-05-01',
    cookies=cookies
):
    print(index)

# 获取百度咨询指数
for index in get_feed_index(
    keywords_list=keywords_list,
    start_date='2018-01-01',
    end_date='2019-05-01',
    cookies=cookies
):
    print(index)
```
  
### Result

```
百度搜索指数: {'keyword': ['抑郁', '自杀', '明星'], 'type': 'wise', 'date': '2018-06-10', 'index': '1835'}
百度媒体指数: {'keyword': ['抑郁', '自杀', '明星'], 'date': '2018-12-29', 'type : 'news', 'index': '0'}
百度咨询指数: {'keyword': ['抑郁', '自杀', '明星'], 'date': '2018-12-29', 'type': 'feed', 'index': '1102911'}
```

### Tips

- 搜索指数最早的数据日期为2011-01-01
- 开始时间超过最早的数据日期会导致数据不准确  
- 初始化类时传入area可以查询指定区域的百度指数, 默认为全国
- 有些代码不是特别严谨, 有需要请自己DIY
- 媒体指数不支持细分地域查询
- 当查询百度指数未收录的关键词时也会出现报错，这个之后会修复

### Changelog

2018/02/10 更新格式化数据的方法format_data  
2018/12/29 更新查询指定区域百度指数的功能  
2018/11/07 更新  
2019/05/31 更新  
2020/02/14 添加咨询指数和媒体指数的功能  
2020/04/16 重构项目结构  
2020/05/08 百度指数修改传递参数  
2020/07/13 添加组合词查询
