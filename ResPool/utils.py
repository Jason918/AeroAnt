__author__ = 'jason'

import hashlib


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