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
  
### update 
2018/11/07 更新

