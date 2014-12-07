__author__ = 'jason'

import res_manager
from clock import Clock
import threading
import sky_client
import utils
import default_functions


def reset():
    res_manager.reset()
    Clock.reset()


def _handle_request(request_content):
    req = sky_client.take(request_content, return_id=True, timeout=60000)
    if req is None:
        print "req is None"
        return
    request, rid = req
    if len(request) != 3:
        print "request format error,request:", request
        return
    func = request[1]
    param = request[2]
    res_value = None
    print "func=", func, "param=", param
    if func == "get_res":
        name, clock = param
        res_value = res_manager.get(name, clock)
    elif func == "add_res":
        name, model, update = param
        if update is None:
            update_function = None
        elif len(update) == 2:
            if update[0] == "PythonFunctionObject":
                update_function = utils.string_to_function(update[1], "update")
            elif update[0] == "DefaultFunction":
                delay = update[1]["delay"]
                cycle = default_functions.get(update[1]["next"], return_type=True)
                res_manager.update_delay(name, delay, cycle)
                update_function = default_functions.get(update[1]["rule"])
            else:
                print "Unknown Update:", update
                return
        else:
            print "Unknown Update:", update
            return
        res_value = res_manager.add(name, model, update_function)
    elif func == "get_clock":
        res_value = Clock.get()
    elif func == "update_res":
        name, cycle, par = param
        res_value = res_manager.update(name, cycle, par)
    elif func == "add_listener":
        ref_res, condition, action = param
        res_manager.add_listener(ref_res,
                                 utils.string_to_function(condition, "condition"),
                                 utils.string_to_function(action, "action"))
    elif func == "ticktock":
        time = int(param)
        for i in range(time):
            tick()
            tock()
    elif func == "reset":
        reset()
    elif func == "set_res_value":
        name, value = param
        res_manager.set_res_value(name, value)
    elif func == "modify_res_value":
        name, delta = param
        res_manager.modify_value(name, delta)
    else:
        print "unknown function:", func
        return
    result = sky_client.get_content(["res_pool_client", func, rid, res_value])
    sky_client.write(result, expire=3000)


def __res_server__():
    request_content = sky_client.get_content(["res_pool", "?", "?"])
    while True:
        try:
            _handle_request(request_content)
        except Exception as e:
            print e


__server_thread__ = threading.Thread(target=__res_server__)


def start():
    # __server_thread__.start()
    __res_server__()


def tick():
    res_manager.changed_res_set.clear()
    res_manager.run_timer()


def tock():
    res_manager.run_listener()
    Clock.tick()
    report()


def report():
    print "-----------------------------------------------------"
    print "CLOCK:", Clock.get()
    res_manager.report()
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"


if __name__ == "__main__":
    start()
    print "started"