import math
import res_manager

__author__ = 'jason'

METHOD_TIME = "Time"
# new method format. type=math
MATH_PREFIX = "math_expression"
METHOD_MATH_ADD = "math_expression#add"
METHOD_MATH_DIVISION = "math_expression#division"
METHOD_MATH_MINUS = "math_expression#minus"
METHOD_MATH_MULTIPLY = "math_expression#multiply"
METHOD_MATH_MOD = "math_expression#mod"
METHOD_MATH_LINEAR = "math_expression#linear"
METHOD_MATH_SIN = "math_expression#sin"
METHOD_MATH_LOG = "math_expression#log"
METHOD_MATH_SUM = "math_expression#sum"
# type = probability
PROBABILITY_PREFIX = "probability"
METHOD_PROBABILITY_MARKOV_CHAIN = "probability#markov_chain"
METHOD_PROBABILITY_SIMPLE_RAND = "probability#simple_rand"
METHOD_PROBABILITY_NORMAL_VARIATE_RAND = "probability#normal_variate_rand"
#type = others
METHOD_OTHERS_COMBINE = "others#combine"
METHOD_OTHERS_DATA_LIST = "others#data_list"

from time import strftime
from clock import Clock
from random import normalvariate, randint, random


def markov_chain(value, states, init_state, transform):
    if value not in states:
        print "invalid state:", value
        return init_state
    cur_index = states.index(value)
    p = random()
    weight_list = transform[cur_index]
    total_weight = sum(weight_list)
    cur_weight = 0.0
    index = 0
    for weight in weight_list:
        cur_weight += weight
        if cur_weight / total_weight > p:
            return states[index]
        index += 1


def get_value(value, v):
    if value == "$slef":
        return v
    elif value == "$clock":
        return Clock.get()
    elif value.startswith("$"):
        return res_manager.get(value[1:])
    else:
        return value


def get(data):
    if "method" not in data:
        print "invalid data for default method"
        return
    method = data["method"]

    if method.startswith(MATH_PREFIX):
        if method == METHOD_MATH_ADD:
            a = data["parameter"]["a"]
            b = data["parameter"]["b"]
            method = lambda value: get_value(a, value) + get_value(b, value)
        elif method == METHOD_MATH_DIVISION:
            a = data["parameter"]["a"]
            b = data["parameter"]["b"]
            method = lambda value: get_value(a, value) / get_value(b, value)
        elif method == METHOD_MATH_MINUS:
            a = data["parameter"]["a"]
            b = data["parameter"]["b"]
            method = lambda value: get_value(a, value) - get_value(b, value)
        elif method == METHOD_MATH_MULTIPLY:
            a = data["parameter"]["a"]
            b = data["parameter"]["b"]
            method = lambda value: get_value(a, value) * get_value(b, value)
        elif method == METHOD_MATH_MOD:
            a = data["parameter"]["a"]
            b = data["parameter"]["b"]
            method = lambda value: get_value(a, value) % get_value(b, value)
        elif method == METHOD_MATH_LINEAR:
            a = data["parameter"]["a"]
            b = data["parameter"]["b"]
            x = data["parameter"]["x"]
            method = lambda value: get_value(a, value) * get_value(x, value) + get_value(b, value)
        elif method == METHOD_MATH_SIN:
            a = data["parameter"]["a"]
            b = data["parameter"]["b"]
            x = data["parameter"]["x"]
            method = lambda value: get_value(a, value) * math.sin(get_value(x, value)) + get_value(b, value)
        elif method == METHOD_MATH_LOG:
            a = data["parameter"]["a"]
            b = data["parameter"]["b"]
            x = data["parameter"]["x"]
            method = lambda value: get_value(a, value) * math.log(get_value(x, value)) + get_value(b, value)
        else:
            print "not support method:", method
    elif method.startswith(PROBABILITY_PREFIX):
        if method == METHOD_PROBABILITY_MARKOV_CHAIN:
            state_set = data["parameter"]["state_set"]
            init_state = data["parameter"]["init_state"]
            trans_matrix = data["parameter"]["trans_matrix"]
            method = lambda value: markov_chain(value, state_set, init_state, trans_matrix)
        elif method == METHOD_PROBABILITY_NORMAL_VARIATE_RAND:
            mu = data["parameter"]["mu"]
            sigma = data["parameter"]["sigma"]
            method = lambda: normalvariate(mu, sigma)
        elif method == METHOD_PROBABILITY_SIMPLE_RAND:
            min_value = data["parameter"]["min"]
            max_value = data["parameter"]["max"]
            method = lambda: randint(min_value, max_value)
        else:
            print "not support method:", method
    else:
        if method == METHOD_OTHERS_COMBINE:
            sections = data["parameter"]["section"]
            method = lambda value: dict((section['name'], get_value(section['value'], value)) for section in sections)
        elif method == METHOD_OTHERS_DATA_LIST:
            data_list = data["parameter"]["data_list"]
            method = lambda value: data_list[Clock.get() % len(data_list)]
        else:
            print "not support method:", method
    return method


