__author__ = 'jason'

from lxml.builder import E
from lxml.etree import tostring
from clock import Clock
import types
import utils


def is_simple_model(model):
    if type(model) is dict and "$schema" in model:
        return False
    else:
        return True


class Res:
    def __init__(self, name, model, update_func):
        self.name = name
        self.model = model
        self.update_func = update_func
        self.value = list()
        # if is_simple_model(model):
        # try :
        # v = eval(model)
        #     except Exception:
        #         v = model
        # else:
        #     print "full schema not support yet."
        self.set_value(model)


    def update(self, param=None):
        arg_cnt = self.update_func.__code__.co_argcount
        if arg_cnt == 0:
            new_value = self.update_func()
        elif arg_cnt == 1:
            new_value = self.update_func(self.get_value())
        else:
            new_value = self.update_func(self.get_value(), param)
        self.set_value(new_value)

    def set_value(self, value):
        self.value.append((Clock.get(), value))

    def get_value(self, clock=-1):
        cur = Clock.get()
        if clock < 0:
            clock = cur + clock

        if clock > cur or clock < 0:
            raise Exception("clock out of range")

        for item in reversed(self.value):
            if item[0] <= clock:
                return item[1]

# format:
# name -> res
pool = dict()

# format :
# clock -> [callback,...]
timers = dict()

# format
# id -> (res_list, condition, action)
listeners = dict()

# format:
# name->[listener_id,]
res_to_listener = dict()

changed_res_set = set()


def add_timer_callback(time, callback):
    utils.get_list(timers, time).append(callback)


def get_res(name):
    if name not in pool:
        return None
    return pool[name]


def get(name, clock=-1):
    return get_res(name).get_value(clock)


def add(name, model, update_func):
    pool[name] = Res(name, model, update_func)


def update(name, cycle=None, param=None):
    changed_res_set.add(name)
    res = get_res(name)
    res.update(param)
    if cycle is not None:
        add_timer_callback(Clock.get() + cycle, lambda: update(name, cycle, param))


def add_listener(res_list, condition, action):
    if not isinstance(condition, types.FunctionType) \
            or not isinstance(condition, types.FunctionType):
        return None

    listener_id = utils.calc_function_hash([condition, action])
    listener = (res_list, condition, action)
    listeners[listener_id] = listener

    for name in res_list:
        utils.get_list(res_to_listener, name).append(listener_id)

    return listener_id


def remove_listener(listener_id):
    if listener_id not in listeners:
        return
    listener = listeners.pop(listener_id)
    res_list = listener[0]
    for name in res_list:
        res_to_listener[name].remove(listener_id)


def run_timer():
    clk = Clock.get()
    if clk not in timers:
        return
    callback_list = timers[clk]
    for callback in callback_list:
        callback()


def run_listener():
    listener_id_set = set()
    for res_name in changed_res_set:
        if res_name in res_to_listener:
            for lid in res_to_listener.get(res_name):
                listener_id_set.add(lid)

    for listener_id in listener_id_set:
        if listener_id in listeners:
            (res_list, condition, action) = listeners.get(listener_id)
            if condition():
                action()


def report():
    for name in pool:
        print name, " = ", pool.get(name).get_value()


def report_xml(file_name="report.xml", clock=-1):
    cur = Clock.get()
    if clock < 0:
        clock += cur
    content = E.content(clock=str(clock))
    for name in pool:
        value = str(pool.get(name).get_value(clock))
        content.insert(0, E.feature(E.name(name), E.currentValue(value)))
    with open(file_name, "w") as fout:
        fout.write(tostring(content, encoding='utf-8', xml_declaration=True, pretty_print=True))




