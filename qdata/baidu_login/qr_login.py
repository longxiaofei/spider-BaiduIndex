from typing import Tuple
from urllib.parse import quote
from base64 import b64encode
import json
import io

import requests
import matplotlib.pyplot as plt

from qdata.errors import QdataError, ErrorCode
from .common import (
    get_gid,
    get_cur_timestamp,
    format_callback_resp,
    get_shaone,
    get_sig
)
from .config import EXIN_TOKEN

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
}

session = requests.session()


def get_qrcode_info() -> Tuple[str, str, str]:
    url = 'https://passport.baidu.com/v2/api/getqrcode'
    params = {
        "lp": "pc",
        "qrloginfrom": "pc",
        "gid": get_gid(),
        "callback": f"tangram_guid_{get_cur_timestamp()}",
        "apiver": "v3",
        "tt": get_cur_timestamp(),
        "tpl": "mn",
        "_": get_cur_timestamp()
    }

    resp = session.get(url, params=params, headers=HEADERS)
    resp_text = format_callback_resp(resp.text)
    resp_data = json.loads(resp_text)
    return (
        "http://" + resp_data["imgurl"],
        resp_data["sign"],
        params["callback"]
    )


def show_qrcode(url: str):
    resp = session.get(url)
    im = plt.imread(io.BytesIO(resp.content))
    plt.imshow(im)
    plt.show()


def get_bduss(sign: str, callback: str) -> str:
    url = "https://passport.baidu.com/channel/unicast"
    params = {
        "channel_id": sign,
        "tpl": "mn",
        "gid": get_gid(),
        "callback": callback,
        "apiver": "v3",
        "tt": get_cur_timestamp(),
        "_": get_cur_timestamp()
    }

    resp = session.get(url, params=params)
    resp_text = format_callback_resp(resp.text)
    resp_data = json.loads(resp_text)

    return json.loads(resp_data['channel_v'])['v']


def get_login_cookie(bduss: str) -> str:
    url = "https://passport.baidu.com/v3/login/main/qrbdusslogin"
    params = {
        "alg": "v3",
        "apiver": "v3",
        "bduss": bduss,
        "loginVersion": "v4",
        "qrcode": 1,
        "time": get_cur_timestamp()//1000,
        "tpl": "mn",
        "tt": get_cur_timestamp(),
        "u": "https%3A%2F%2Fwww.baidu.com%2F"
    }

    params['sig'] = get_sig(params)
    params['shaOne'] = get_shaone()
    params['elapsed'] = 1234
    params['v'] = params['tt']
    params['callback'] = "bd__cbs__odmford"

    session.get(url, params=params, headers=HEADERS)

    urls = [
        "https://www.baidu.com/",
        "http://index.baidu.com/api/SugApi/sug",
    ]
    for url in urls:
        session.get(url, headers=HEADERS)
    cookies = '; '.join([
        f"{cookie.name}={cookie.value}"
        for cookie in session.cookies
    ])
    return cookies


def get_exin() -> str:
    """
    拿恶心的东西
    """
    url = "https://miao.baidu.com/abdr"
    resp = session.post(url, data=EXIN_TOKEN, headers=HEADERS)
    resp_data = json.loads(resp.text)
    if isinstance(resp_data['data'], dict):
        return "; __yjsv5_shitong={}_{}_{}_{}_{}_{}_{}".format(
            resp_data['data']['ver'],
            resp_data['key_id'],
            resp_data['data']['lid'],
            resp_data['data']['ret_code'],
            resp_data['data']['server_time'],
            resp_data['data']['ip'],
            resp_data['sign']
        )
    elif isinstance(resp_data['data'], str):
        __yjs_st = b64encode(quote("_".join([resp_data['data'], resp_data['key_id'], resp_data['sign']])).encode()).decode()
        return "; __yjs_st=2_{}".format(__yjs_st)
    else:
        raise QdataError(ErrorCode.LOGIN_FAIL)


def get_cookie_by_qr_login() -> str:
    print("扫完码记得关闭弹出的图片框...")

    try:
        qrcode_link, sign, callback = get_qrcode_info()
        show_qrcode(qrcode_link)
    except Exception:
        raise QdataError(ErrorCode.GET_QR_FAIL)

    try:
        bduss = get_bduss(sign, callback)
        cookies = get_login_cookie(bduss)
    except Exception:
        raise QdataError(ErrorCode.LOGIN_FAIL)

    try:
        cookies = cookies + get_exin()
    except Exception:
        raise QdataError(ErrorCode.INDEX_LOGIN_FAIL)

    return cookies
