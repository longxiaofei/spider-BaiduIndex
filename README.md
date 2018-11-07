## 百度指数爬虫

### Why make this script?
因为有个傻子竟然要去淘宝买百度指数的数据，听说一条好几块钱呢

### Thinking
~~看了一下github关于百度指数的项目，分为两种:~~ 
- ~~第一种是通过selenium操作浏览器进入搜索页，等待浏览器加载完所有资源后~~  
~~通过执行PPval.ppt,PPval.res2来获取res和res2的值~~  
~~再进行后面一系列的操作~~
- ~~第二种是通过selenium操作浏览器进入搜索页，通过模拟鼠标移动的形式，~~  
~~不断定位指数图片出现的位置，截取图片进行识别~~
  
~~我们将改进第一种方法~~
  
2018-11-02：百度指数改版了，我们不改进第一种方法了！通过模拟鼠标移动的方式来获取数据，真香~~

### Requirements
python3.5+
  
requests  
selenium  
~~Pillow~~  
~~pytesseract~~  

### Use
下载chromedriver, 并将它放到环境变量中  
单账号抓取：请你打开百度的首页，登录后，将百度首页的cookie复制后，粘贴到config.py中的COOKIES对象中  
~~下载tesseract, 并将它放到环境变量中~~  
~~找到tesseract文件夹, tesseract/3.05.02/share/tessdata/configs中的digits~~  

#### baidu_spider
unable  

#### new_spider_20181102
之后在demo.py写入以下代码  
kind=0为搜索指数爬取  
kind=1为资讯指数爬取
```
from new_get_index import main

if __name__ == "__main__":
    demo = main('张艺兴', '2018-01-01', '2018-09-01', kind=0)
    for data in demo:
        print(data)
```
  
#### new_spider_without_selenium
之后在demo.py写入以下代码  
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

### Demo
![image](https://github.com/longxiaofei/markdown_img/blob/master/spider-baiduindex/bbb.png?raw=true)
  
### Process
~~1. 通过requests向搜索页发送请求,获取搜索页的html~~  
~~2. 解析第1步中的html,可以直接得到res1的值,并且通过一些小技巧拿到res2的js加密代码~~  
~~3. 使用selenium,加载下载到本地的Raphael.js(res2加密必须的js，而这个代码必须在浏览器环境下运行),并运行第2步得到~~  
~~的res2加密代码，得到res2~~  
~~4. 使用res1、res2、开始日期、结束日期构造获取res3的url，并发送请求~~  
~~5. 解析第4步得到的html,获取res3列表~~  
~~6. 使用res1、res2、res3构造url获取百度指数的html代码~~  
~~7. 使用浏览器渲染第6步得到的html代码,并进行截取~~  
~~8. 使用pytesseract识别图片,得到指数~~  
#### selenium
1. 获取时间范围，以300天为一个时间段，将时间分为若干段
2. 模拟鼠标操作修改百度指数的时间范围
3. 模拟鼠标移动，获取渲染后的html数据
4. 重复2、3步，直到获取全部数据
 
#### 直接请求
...  
 
### Tip
- ~~虽然使用了selenium，但是没有使用selenium发送任何网络请求~~
- ~~过程中没有产生额外的文件，html是使用js操作dom渲染的,图片是走的io流~~
- ~~js加密代码中的变量和过程是由后端随机生成，所以不能写死，所以每次请求将会自动抽取js加密代码~~
- ~~这个脚本没有实现自动获取cookie的功能, 如需要多账号抓取, 请自行实现~~
- 搜索指数最早的数据日期为2011-01-01
- 咨询指数最早的数据日期为2017-07-03
- 开始时间超过最早是数据日期会导致数据不准确

### Error
~~在本机测试时，chromedriver是按照1px=2px来显示的,目前不清楚是什么问题导致的。~~  
~~目前代码已改成1px=1px来截取指数图片了。~~  

### Todo
no

### update
2018/11/03 更新  
2018/11/05 增加资讯指数爬取  
2018/11/06 修正获取时间范围方法  
2018/11/07 更新直接发送http请求获取数据的方法[spider_without_selenium](https://github.com/longxiaofei/spider-BaiduIndex/tree/master/new_spider_without_selenium)  

