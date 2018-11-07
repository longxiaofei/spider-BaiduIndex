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

