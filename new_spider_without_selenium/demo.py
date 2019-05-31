from get_index import BaiduIndex

if __name__ == "__main__":
    keywords = ['爬虫', 'lol', '张艺兴', '人工智能', '华为', '武林外传']
    baidu_index = BaiduIndex(keywords, '2018-01-01', '2019-05-02')
    for index in baidu_index.get_index():
        print(index)
