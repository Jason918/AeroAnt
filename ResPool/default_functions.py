__author__ = 'jason'

METHOD_TIME = "Time"
METHOD_RANDINT = "Randint"
METHOD_FINITE_STATE_MACHINE = "FiniteStateMachine"
METHOD_NORMAL_VARIATE = "NormalVariate"
METHOD_LINEAR_CLOCK = "LinearClock"
# METHOD_POLYNOMIAL_CLOCK = "PolynomialClock"
from time import strftime
from clock import Clock
from random import normalvariate,randint,random


def finite_state_machine(value, states, transform):
    if value not in states:
        print "invalid state:", value
        return None
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


def get(data):
    if "method" not in data:
        print "invalid data for default method"
        return
    method = data["method"]
    if method == METHOD_TIME:
        format = data["format"]
        method = lambda: strftime(format)
    elif method == METHOD_FINITE_STATE_MACHINE:
        states = data["states"]
        transform = data["transform"]
        method = lambda value: finite_state_machine(value, states,transform)
    elif method == METHOD_LINEAR_CLOCK:
        slope = data["slope"]
        intersection = data["intersection"]
        method = lambda: Clock.get() * slope + intersection
    elif method == METHOD_NORMAL_VARIATE:
        mu = data["mu"]
        sigma = data["sigma"]
        method = lambda: normalvariate(mu, sigma)
    elif method == METHOD_RANDINT:
        min = data["min"]
        max = data["max"]
        method = lambda: randint(min, max)
    # elif method == METHOD_POLYNOMIAL_CLOCK:
    else:
        print "not support method:", method

    return method


