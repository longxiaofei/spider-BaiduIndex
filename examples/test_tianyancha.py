import time
from datetime import datetime
from queue import Queue

from qdata.tianyancha.company_filter_options import (
    get_category_data,
    get_area_data,
    get_reg_status,
    get_capital_unit,
    get_company_type,
    get_institution_type,
    get_financing_round,
    get_listed_type
)
from qdata.tianyancha import get_company_count
from qdata.errors import QdataError


def test_filter_options():
    # 获取全部分类
    print(get_category_data())
    # 获取全部地区
    print(get_area_data())
    # 获取全部注册状态
    print(get_reg_status())
    # 获取资本类型
    print(get_capital_unit())
    # 获取公司类型
    print(get_company_type())
    # 机构类型
    print(get_institution_type())
    # 获取融资轮次
    print(get_financing_round())
    # 获取上市状态
    print(get_listed_type())


def _get_category_dict():
    data = get_category_data()
    level2_category_dict = {}
    for level1_category in data:
        for level2_category in level1_category["children"]:
            value = level2_category["value"]
            level2_category_dict[value] = [
                level1_category["label"],
                level2_category["label"]
            ]
    return level2_category_dict


def _get_area_dict():
    data = get_area_data()
    level1_area_dict = {}
    for level1_area in data:
        value = level1_area["value"]
        level1_area_dict[value] = [
            level1_area["label"]
        ]
    return level1_area_dict


def test_get_company_count_0():
    """查看如何传参, 我不清楚为啥提示提示时我的注解被吞掉了"""
    print(get_company_count.__annotations__)


def test_get_company_count_1():
    """
        查询 <各省市><各二级行业><50人以上和100以上><存续><除个体工商户和港澳台组织>的公司个数
        数据示例:{'所在省': '北京市', '一级行业': '农、林、牧、渔业', '二级行业': '农业', '公司人数': '50人以上', '公司个数': 24}
    """
    category_dict = _get_category_dict()
    area_dict = _get_area_dict()
    staff_num_range_dict = {
        (50, -1): "50人以上",
        (100, -1): "100人以上"
    }
    q = Queue()

    for category in category_dict.keys():
        for area in area_dict.keys():
            for staff_num_range in staff_num_range_dict.keys():
                params = {
                    "area_code": area,
                    "category": category,
                    "staff_num_range": staff_num_range
                }
                q.put(params)

    while q.empty() is False:
        params = q.get()
        area = params["area_code"]
        category = params["category"]
        staff_num_range = params["staff_num_range"]

        try:
            count = get_company_count(
                area_code=[area],
                category=[category],
                staff_num_range=[staff_num_range],
                reg_status=["存续（在营、开业、在业）"],
                company_type=["私营企业", "联营企业", "外商投资企业", "普通合伙", "有限合伙", "国有企业", "股份有限公司", "有限责任公司"]
            )
        except QdataError:
            q.put(params)
            time.sleep(100)
            continue

        data = {
            "所在省": area_dict[area][0],
            "一级行业": category_dict[category][0],
            "二级行业": category_dict[category][1],
            "公司人数": staff_num_range_dict[staff_num_range],
            "公司个数": count
        }
        print(data)
        time.sleep(1.7)


def test_get_company_count_2():
    """
    查询
    <地区>在山东和河南
    <行业>为采矿业
    <注册资本>在5000万以上
    <成立时间>5年前成立的
    <公司类型>有限责任公司
    <有无联系方式>有
    的公司个数
    """
    count = get_company_count(
        area_code=["370000", "410000"],
        category=["B"],
        reg_capital_range=[(5000, -1)],
        establish_time_range=[
            (-1, int(datetime.now().replace(datetime.now().year - 5).timestamp()*1000))
        ],
        company_type=["有限责任公司"],
        has_phone=True
    )
    print(count)


if __name__ == "__main__":
    test_get_company_count_0()
    # test_get_company_count_1()
    test_get_company_count_2()
