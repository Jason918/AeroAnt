__author__ = 'jason'
import requests
import hashlib
import json
import base64

SKY_SERVER = "http://127.0.0.1:9000"
WRITE_URL = "/skyentry/write"
READ_URL = "/skyentry/read"
TAKE_URL = "/skyentry/take"


def __encode(item):
    if item == "?":
        return "?"
    else:
        json_str = json.dumps(item)
        return base64.b64encode(json_str)


def __decode(item):
    if item == "?":
        return "?"
    else:
        return json.loads(base64.b64decode(item))


def __handle_result(r, is_multi, return_id):
    ret = r.json()
    if not is_multi:
        if len(ret) > 1:
            print "sky drop too many results!"
        ret = ret[0]
        content = ret["content"].split(",")
        result = map(__decode, content)

        if return_id:
            rid = hashlib.sha1(ret["content"]).hexdigest()
            return result, rid
        else:
            return result
    else:
        print "not implement yet"
        return None


def write(content, type=-1, expire=3000):
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

    result = __handle_result(r, is_multi, return_id)
    print "READ:", result
    return result


def take(content, is_multi=False, timeout=500, return_id=False):
    param = {
        "content": content,
        "isMulti": is_multi,
        "timeout": timeout
    }
    r = requests.get(SKY_SERVER + TAKE_URL, params=param)
    result = __handle_result(r, is_multi, return_id)
    print "TAKE:", result
    return result


def get_content(item_list, return_id=False):
    print "get_content:", item_list, return_id
    content = ",".join(map(__encode, item_list))
    if return_id:
        cid = hashlib.sha1(content).hexdigest()
        return content, cid
    else:
        return content
