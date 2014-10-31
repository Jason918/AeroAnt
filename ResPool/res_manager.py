__author__ = 'jason'

from clock import Clock
import types
import utils


def is_simple_model(model):
    if type(model) is dict and model.has_key("$schema"):
        return False
    else:
        return True


class Res:
    def __init__(self, name, model, update):
        self.name = name
        self.model = model
        self.update = update
        self.value = list()
        if is_simple_model(model):
            self.set_value(model)

    def update(self, param):
        self.set_value(self.update(param))

    def set_value(self, value):
        self.value.append((Clock.get(), value))

    def get(self, clock):
        cur = Clock.get()
        if clock < 0:
            clock = cur - clock

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
#     name->[listener_id,]
res_to_listener = dict()

changed_res_set = set()


def add_timer_callback(time, callback):
    if timers[time] is None:
        timers[time] = list()
    timers[time].append(callback)


def get(name, clock=-1):
    if not pool.has_key(name):
        return None
    res = pool[name]
    return res.get(clock)


def add(name, model, update_func):
    pool[name] = Res(name, model, update_func)


def update(name, cycle=None, param=None):
    changed_res_set.add(name)
    res = get(name)
    res.update(param)
    if cycle is not None:
        add_timer_callback(Clock.get() + cycle, lambda: update(name, cycle, param))


def add_listener(res_list, condition, action):
    if type(condition) is not types.FunctionType or type(condition) is not types.FunctionType:
        return None

    listener_id = utils.calc_function_hash([condition, action])
    listener = (res_list, condition, action)
    listeners[listener_id] = listener

    for name in res_list:
        utils.get_list(res_to_listener, name).append(listener_id)

    return listener_id


def remove_listener(listener_id):
    if not listeners.has_key(listener_id):
        return
    listener = listeners.pop(listener_id)
    res_list = listener[0]
    for name in res_list:
        res_to_listener[name].remove(listener_id)


def run_timer():
    clk = Clock.get()
    if not timers.has_key(clk):
        return
    callback_list = timers[clk]
    for callback in callback_list:
        callback()


def run_listener():
    listener_id_set = set()
    for res_name in changed_res_set:
        if res_to_listener.has_key(res_name):
            listener_id_set += res_to_listener.get(res_name)

    for listener_id in listener_id_set:
        if listeners.has_key(listener_id):
            (res_list, condition, action) = listeners.get(listener_id)
            if condition():
                action()




