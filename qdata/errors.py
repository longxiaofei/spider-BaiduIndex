from enum import Enum


class ErrorCode(int, Enum):
    NO_LOGIN = 10001
    UNKNOWN = 10002
    NETWORK_ERROR = 10003

    KEYWORD_LIMITED = 20001


CODE_MSG_MAP = {
    ErrorCode.NO_LOGIN: 'cookies失效，请重新获取cookies',
    ErrorCode.UNKNOWN: '未知错误',
    ErrorCode.NETWORK_ERROR: '网络错误',
    ErrorCode.KEYWORD_LIMITED: ('关键词最多传递5个, '
                                '可以使用`from baidu.index.common import split_keywords`,'
                                '对关键词进行切分')
}


class QdataError(Exception):
    def __init__(self, code: ErrorCode):
        self.code = code
        self.msg = CODE_MSG_MAP.get(code)

    def __str__(self):
        return repr(f"ERROR-{self.code}: {self.msg}")
