from collections import defaultdict
import marshal
import hashlib
import types
import base64

from clock import Clock
from random import random
from xml.etree import cElementTree as ET

__author__ = 'jason'


def calc_function_hash(func_list):
    s = ""
    for f in func_list:
        s += f.__code__.co_code
    return hashlib.sha1(s).hexdigest()


def get_set(dic, key):
    if key not in dic:
        dic[key] = set()
    return dic[key]


def get_list(dic, key):
    if key not in dic:
        dic[key] = list()
    return dic[key]


def function_to_string(func):
    if func is None:
        return None
    if not is_function(func):
        raise Exception("func is not callable!")
    code_str = marshal.dumps(func.func_code)
    return base64.b64encode(code_str)


def string_to_function(string, function_name="func"):
    if string is None:
        return None
    string = base64.b64decode(string)
    code = marshal.loads(string)
    from res_manager import get

    func = types.FunctionType(code, dict(globals().items() + locals().items()), function_name)
    return func


def is_function(func):
    return hasattr(func, '__call__')


def get_data_from_xml(file_path):
    with open(file_path, "r") as fin:
        context = fin.read()
        t = ET.XML(context)
        return etree_to_dict(t)


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def warp_update_value(func):
    """

    :param func:
    :return: format:
    {
        "function": function name,
        "parameter": {
            some parameter: parameter value,
            ...
        }
    }
    """
    if "function" not in func:
        return func
    ret = dict()
    f = func["function"]
    ret["method"] = f["@type"] + "#" + f["@name"]
    p = dict()
    ret["parameter"] = p
    if type(f["parameter"]) is not list:
        p[f["parameter"]["@name"]] = f["parameter"]["#text"]
    else:
        for param in f["parameter"]:
            if param["@name"] in p:
                p[param["@name"]] = [p[param["@name"]], warp_update_value(param["#text"])]
            else:
                p[param["@name"]] = warp_update_value(param["#text"])
    return ret


def warp_update(update):
    ret = dict()
    ret["delay"] = int(update["delay"])
    ret["next"] = warp_update_value(update["next"])
    ret["rule"] = warp_update_value(update["rule"])
    return ret
