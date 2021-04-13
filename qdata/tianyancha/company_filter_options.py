from typing import List, Dict
import os
import json

cur_dir_path = os.path.dirname(os.path.abspath(__file__))


def get_category_data() -> List[Dict]:
    """分类数据"""
    data_file = os.path.join(cur_dir_path, "base_datas", "category")
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_area_data() -> List[Dict]:
    """地区数据"""
    data_file = os.path.join(cur_dir_path, "base_datas", "area")
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_reg_status() -> List[str]:
    """注册状态"""
    return ["迁出", "迁入", "撤销", "停业", "注销", "吊销", "存续（在营、开业、在业）"]


def get_capital_unit() -> List[int]:
    """资本类型, 1人民币, 2美元, 3其他
    """
    return [1, 2, 3]


def get_company_type() -> List[str]:
    """公司类型"""
    return [
        "私营企业", "联营企业", "港、澳、台", "外商投资企业", "普通合伙", "有限合伙", "个人独资企业",
        "个体工商户", "国有企业", "股份合作制", "集体所有制", "股份有限公司", "有限责任公司"
    ]


def get_institution_type() -> List[str]:
    """
    机构类型
    "tw"             台湾省企业
    "hk"             香港特别行政区企业
    "lawFirm"        律所
    "npo"            社会组织
    "npo_foundation" 基金会
    "institution"    事业单位
    "normal_company" 企业
    """
    return ["tw", "hk", "lawFirm", "npo", "npo_foundation", "institution", "normal_company"]


def get_financing_round() -> List[str]:
    """融资轮次"""
    return [
        "IPO上市", "C轮及以上", "PreB至B+轮", "PreA至A+轮", "天使/种子轮", "未融资",
        "其它", "定向增发", "股权融资/转让", "战略融资/投资", "并购/合并"
    ]


def get_listed_type() -> List[str]:
    """上市状态"""
    return ["新四板", "新三板", "科创板", "港股", "中概股", "A股", "未上市"]
