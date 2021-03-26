from datetime import datetime
from base64 import b64encode
from typing import Dict
import re
import uuid
import hashlib

from Crypto.Cipher import AES


def _padding_pkcs7(m: str) -> str:
    return m+chr(16-len(m)%16)*(16-len(m)%16)


def get_cur_timestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


def get_gid() -> str:
    return str(uuid.uuid4()).upper()


def format_callback_resp(resp_text: str) -> str:
    return re.search(r'\((.*?)\)', resp_text)[1]


def get_shaone() -> str:
    cur_timestamp = str(int(datetime.now().timestamp() * 1000))
    m5 = hashlib.md5(cur_timestamp.encode()).hexdigest()
    return hashlib.sha1(m5.encode()).hexdigest()


def get_sig(params: Dict) -> str:
    text = '&'.join([
        f"{key}={value}"
        for key, value in params.items()
    ])
    m5 = hashlib.md5(text.encode()).hexdigest()
    insert_string = "tnrstsms"
    final_text_start = ''.join([
        s + e
        for s, e in zip(m5[:8], insert_string)
    ])
    final_text = final_text_start + m5[8:]

    aes = AES.new("moonshad8moonsh6".encode(), AES.MODE_ECB)
    first_base64 = b64encode(
        aes.encrypt(_padding_pkcs7(final_text).encode())
    )
    return b64encode(first_base64).decode()
