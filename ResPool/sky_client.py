__author__ = 'jason'
import requests

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


def read(content, isMulti=False, timeout=500):
    param = {
        "content": content,
        "isMulti": isMulti,
        "timeout": timeout
    }
    r = requests.get(SKY_SERVER + READ_URL, params=param)
    return r.json()


def take(content, isMulti=False, timeout=500):
    param = {
        "content": content,
        "isMulti": isMulti,
        "timeout": timeout
    }
    r = requests.get(SKY_SERVER + TAKE_URL, params=param)
    return r.json()
