from enum import Enum


class ErrorCode(int, Enum):
    UNKNOWN = 10002
    NETWORK_ERROR = 10003

    # 百度指数
    NO_LOGIN = 20000
    KEYWORD_LIMITED = 20001

    # 百度的登录
    GET_QR_FAIL = 20010
    LOGIN_FAIL = 20011
    INDEX_LOGIN_FAIL = 20012

    # 天眼查
    TYC_COMPANY_COUNT_FAIL = 20020


CODE_MSG_MAP = {
    ErrorCode.NO_LOGIN: 'cookies失效，请重新获取cookies',
    ErrorCode.UNKNOWN: '未知错误',
    ErrorCode.NETWORK_ERROR: '网络错误',
    ErrorCode.KEYWORD_LIMITED: ('关键词最多传递5个, '
                                '可以使用`from qdata.baidu_index.common import split_keywords`,'
                                '对关键词进行切分'),
    ErrorCode.GET_QR_FAIL: "获取二维码失败",
    ErrorCode.LOGIN_FAIL: "百度登录失败",
    ErrorCode.INDEX_LOGIN_FAIL: "百度指数登录失败",
    ErrorCode.TYC_COMPANY_COUNT_FAIL: "获取天眼查公司数量失败"
}


class QdataError(Exception):
    def __init__(self, code: ErrorCode):
        self.code = code
        self.msg = CODE_MSG_MAP.get(code)

    def __str__(self):
        return repr(f"ERROR-{self.code}: {self.msg}")
