from typing import List, Tuple
import json

import requests

from qdata.errors import QdataError, ErrorCode

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}


def get_company_count(
    *,
    area_code: List[str] = None,
    category: List[str] = None,
    reg_capital_range: List[Tuple[int, int]] = None,
    establish_time_range: List[Tuple[int, int]] = None,
    reg_status: List[str] = None,
    capital_unit: List[str] = None,
    company_type: List[str] = None,
    institution_type: List[str] = None,
    staff_num_range: List[Tuple[int, int]] = None,
    financing_round: List[str] = None,
    listed_type: List[str] = None,
    has_phone: bool = None,
    has_mobile: bool = None,
    has_email: bool = None,
    has_brand: bool = None,
    has_dishonest: bool = None,
    has_website: bool = None,
    has_chattel_mortage: bool = None,
    has_copyright: bool = None,
    has_soft_copyright: bool = None,
    is_high_tech_company: bool = None,
    is_tax_a_level: bool = None,
    is_general_taxpayer: bool = None,
    has_bid: bool = None
) -> int:
    """
    area_code: 所在地区\n
    category: 行业分类\n
    reg_capital_range: 注册资本范围(万元)\n
    establish_time_range: 成立时间范围(毫秒)\n
    reg_status: 注册状态\n
    capital_unit: 资本类型\n
    company_type: 企业类型\n
    institution_type: 机构类型\n
    staff_num_range: 员工参保人数范围(人)\n
    financing_round: 融资轮次\n
    listed_type: 上市类型\n
    has_phone: 有无联系方式\n
    has_mobile: 有无手机号\n
    has_email: 有无邮箱\n
    has_brand: 有无商标\n
    has_dishonest: 有无失信\n
    has_website: 有无网址\n
    has_chattel_mortage: 有无动产抵押\n
    has_copyright: 有无作品著作\n
    has_soft_copyright: 有无软件著作\n
    is_high_tech_company: 是否是高新技术企业\n
    is_tax_a_level: 是否税务评级为A\n
    is_general_taxpayer: 是否为一般纳税人\n
    has_bid: 是否有招投标\n
    """
    if reg_capital_range:
        reg_capital_range = [
            num
            for num_tuple in reg_capital_range
            for num in num_tuple
        ]
    if establish_time_range:
        establish_time_range = [
            num
            for num_tuple in establish_time_range
            for num in num_tuple
        ]
    if staff_num_range:
        staff_num_range = [
            num
            for num_tuple in staff_num_range
            for num in num_tuple
        ]
    query = {
        "areaCodeSet": area_code,
        "categoryGuobiao2017Set": category,
        "regCapitalRangeSet": reg_capital_range,
        "establishTimeRangeSet": establish_time_range,
        "regStatusSet": reg_status,
        "capitalUnitSet": capital_unit,
        "companyTypeSet": company_type,
        "institutionTypeSet": institution_type,
        "staffNumRangeSet": staff_num_range,
        "financingRoundList": financing_round,
        "listedTypeSet": listed_type,
        "hasPhone": has_phone,
        "hasMobile": has_mobile,
        "hasEmail": has_email,
        "hasBrand": has_brand,
        "hasDishonest": has_dishonest,
        "hasWebSite": has_website,
        "hasChattelMortage": has_chattel_mortage,
        "hasCopyright": has_copyright,
        "hasSoftCopyright": has_soft_copyright,
        "isHighTechCompany": is_high_tech_company,
        "taxLevel": is_tax_a_level,
        "isGeneralTaxpayer": is_general_taxpayer,
        "hasBid": has_bid
    }

    final_query = {"searchType": 2}
    for key, value in query.items():
        if value is None:
            continue
        if isinstance(value, bool):
            final_query[key] = str(int(value))
        else:
            final_query[key] = value

    url = "https://capi.tianyancha.com/cloud-tempest/advance"
    try:
        resp = requests.post(url, json=final_query, headers=headers)
    except Exception:
        raise QdataError(ErrorCode.TYC_COMPANY_COUNT_FAIL)
    resp_data = json.loads(resp.text)
    return int(resp_data['data']['realTotal'])
