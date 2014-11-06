__author__ = 'jason'
import requests
import hashlib

SKY_SERVER = "http://127.0.0.1:9000"
WRITE_URL = "/skyentry/write"
READ_URL = "/skyentry/read"
TAKE_URL = "/skyentry/take"


def write(content, type=-1, expire=30000):
    param = {
        "content": content,
        "type": type,
        "expire": expire
    }
    r = requests.get(SKY_SERVER + WRITE_URL, params=param)
    return r.json()


def read(content, is_multi=False, timeout=500, return_id=False):
    param = {
        "content": content,
        "isMulti": is_multi,
        "timeout": timeout
    }
    r = requests.get(SKY_SERVER + READ_URL, params=param)
    return r.json()


def take(content, is_multi=False, timeout=500, return_id=False):
    param = {
        "content": content,
        "isMulti": is_multi,
        "timeout": timeout
    }
    r = requests.get(SKY_SERVER + TAKE_URL, params=param)
    if return_id:
        rid = hashlib.sha1(r.text())
        return r.json, rid
    else:
        return r.json()


def get_content(tuple_list, return_id=False):
    content = ",".join(tuple_list)
    if return_id:
        cid = hashlib.sha1(content)
        return content, cid
    else:
        return content
