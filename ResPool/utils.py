import marshal
import hashlib
import types
import base64

from clock import Clock
from random import random

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
