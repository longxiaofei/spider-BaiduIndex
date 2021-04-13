# Qdata - Python SDK for index and search

### 为什么给项目改了名

* 想做一个提供更多数据的SDK包,但不一定有时间。。。
* 老的代码包可以在<a href="https://github.com/longxiaofei/spider-BaiduIndex/tree/old_baiduindex">old_baiduindex</a>里找到
* 会根据我自己个人的数据需求，往里面添加不同的数据源，如果恰好帮助到你，很开心
* 老的数据源会尽力维护

### Data Source

* http://index.baidu.com/
* http://www.baidu.com/
* https://www.tianyancha.com/advance/search

### Install

```shell script
pip uninstall pycrypto  # 避免与pycryptodome冲突
pip install --upgrade qdata
```

### Examples

#### 百度指数
`./examples/test_baidu_index.py`

#### 百度搜索
`./examples/test_baidu_search.py`

#### 百度登录(获取百度Cookie)
`./examples/test_baidu_login.py`

* 目前只提供二维码登录，密码账号登录也可以做，但不做，因为没必要。
* 幸好工作不做爬虫，心太累了。

#### 天眼查
`./examples/test_tianyancha.py`

* 老婆做汇报着急用

### Changelog

* 2021/03/25 上线
* 2021/03/26 更新百度登录功能
* 2021/04/07 百度指数新增:实时百度指数
* 2021/04/13 添加天眼查高级搜索公司数数据
