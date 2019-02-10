### Requirements
python3.5+
  
requests  

### Use
单账号抓取：请你打开百度的首页，登录后，将百度首页的cookie复制后，粘贴到config.py中的COOKIES对象中  
  
在demo.py写入以下代码    
```
from get_index import BaiduIndex

if __name__ == "__main__":
    """
    最多一次请求5个关键词
    """
    
    # 查看城市和省份的对应代码
    print(BaiduIndex.city_code)
    print(BaiduIndex.province_code)

    baidu_index = BaiduIndex(['张艺兴', 'lol', '极限挑战', '吃鸡'], '2016-10-01', '2018-10-02')
    for data in baidu_index('lol', 'all'):
        print(data)

    # 获取全部5个关键词的全部数据
    print(baidu_index.result)
    # 获取1个关键词的全部数据
    print(baidu_index.result['极限挑战'])
    # 获取1个关键词的移动端数据
    print(baidu_index.result['极限挑战']['wise'])
    # 获取1个关键词的pc端数据
    print(baidu_index.result['极限挑战']['pc'])
```
  
### Process
...  
  
### Tip
- 搜索指数最早的数据日期为2011-01-01
- 开始时间超过最早的数据日期会导致数据不准确  
- 初始化类时传入area可以查询指定区域的百度指数, 默认为全国
  
### update 
2018/02/10 更新格式化数据的方法format_data  
2018/12/29 更新查询指定区域百度指数的功能  
2018/11/07 更新

