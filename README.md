### Why make this script?
因为有个傻子竟然要去淘宝买百度指数的数据，听说一条好几块钱呢

### Thinking
看了一下github关于百度指数的项目，分为两种:  
- 第一种是通过selenium操作浏览器进入搜索页，等待浏览器加载完所有资源后  
通过执行PPval.ppt,PPval.res2来获取res和res2的值  
再进行后面一系列的操作
- 第二种是通过selenium操作浏览器进入搜索页，通过模拟鼠标移动的形式，  
不断定位指数图片出现的位置，截取图片进行识别  
  
我们将改进第一种方法  

### Requirements
python3.5+
  
requests  
pytesseract  
selenium  
Pillow  

### Use
下载chromedriver, 并将它放到环境变量中  
下载tesseract, 并将它放到环境变量中  
单账号抓取：请你打开百度的首页，登录后，将百度首页的cookie复制后，粘贴到config.py中的COOKIES对象中  
之后在demo.py写入以下代码
```
from get_index import main

if __name__ == "__main__":
    demo = main('张艺兴', '2018-01-01', '2018-09-01')
    for data in demo:
        print(data)
```

### Demo
![image](https://github.com/longxiaofei/markdown_img/blob/master/spider-baiduindex/bbb.png?raw=true)
  
### Process
1. 通过requests向搜索页发送请求,获取搜索页的html
2. 解析第1步中的html,可以直接得到res1的值,并且通过一些小技巧拿到res2的js加密代码
3. 使用selenium,加载下载到本地的Raphael.js(res2加密必须的js，而这个代码必须在浏览器环境下运行),并运行第2步得到
的res2加密代码，得到res2
4. 使用res1、res2、开始日期、结束日期构造获取res3的url，并发送请求
5. 解析第4步得到的html,获取res3列表
6. 使用res1、res2、res3构造url获取百度指数的html代码
7. 使用浏览器渲染第6步得到的html代码,并进行截取
8. 使用pytesseract识别图片,得到指数
 
### Tip
- 虽然使用了selenium，但是没有发送任何网络请求
- 过程中没有产生额外的文件，html是使用js操作dom渲染的,图片是走的io流
- js加密代码中的变量和过程是由后端随机生成，所以不能写死，所以每次请求将会自动抽取js加密代码
- 这个脚本没有实现自动获取cookie的功能, 如需要多账号抓取, 请自行实现

### Todo
upload code
