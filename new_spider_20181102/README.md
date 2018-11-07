
### Use
下载chromedriver, 并将它放到环境变量中  
单账号抓取：请你打开百度的首页，登录后，将百度首页的cookie复制后，粘贴到config.py中的COOKIES对象中  
  
在demo.py写入以下代码    
```
from new_get_index import main

if __name__ == "__main__":
    """
        kind=0为搜索指数爬取   
        kind=1为资讯指数爬取
    """
    demo = main('张艺兴', '2018-01-01', '2018-09-01', kind=0)
    for data in demo:
        print(data)
```
  
### Demo
![image](https://github.com/longxiaofei/markdown_img/blob/master/spider-baiduindex/bbb.png?raw=true)
  
### Process
1. 获取时间范围，以300天为一个时间段，将时间分为若干段
2. 模拟鼠标操作修改百度指数的时间范围
3. 模拟鼠标移动，获取渲染后的html数据
4. 重复2、3步，直到获取全部数据
  
### Tip
- 搜索指数最早的数据日期为2011-01-01
- 咨询指数最早的数据日期为2017-07-03
- 开始时间超过最早的数据日期会导致数据不准确  
  
### update
2018/11/03 更新  
2018/11/05 增加资讯指数爬取  
2018/11/06 修正获取时间范围方法

