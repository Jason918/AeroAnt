__author__ = 'jason'

from clock import Clock


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


pool = dict()


def get(name, clock=-1):
    if not pool.has_key(name):
        return None
    res = pool[name]
    return res.get(clock)


def add(name, model, update):
    exec update
    update_func = update
    pool[name] = Res(name, model, update_func)


