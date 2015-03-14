import logging
import traceback
import time
import protocal #from ResPool import protocal

__author__ = 'jason'

import res_manager
from clock import Clock
import threading
import sky_client
import utils
import default_functions
from protocal import *

import default_condition


def log():
    return logging.getLogger(__name__)


def reset():
    sky_client.reset()
    res_manager.reset()
    Clock.reset()


def handle_add_res(name, model, update):
    update_function = None
    if type(update) is dict:
        if FUNCTION_TYPE_CALLABLE in update:
            update_function = utils.string_to_function(update[FUNCTION_TYPE_CALLABLE], "update")
        elif FUNCTION_TYPE_DEFAULT in update:
            update_info = update[FUNCTION_TYPE_DEFAULT]
            delay = update_info["delay"]
            cycle = default_functions.get(update_info["next"], return_type='lambda')
            res_manager.update_delay(name, delay, cycle)
            update_function = default_functions.get(update_info["rule"])

    return res_manager.add(name, model, update_function)


def handle_ticktock(time):
    ts = int(time * 2)
    for i in range(ts):
        tick_or_tock()


def handle_add_event_listener(event_id, ref_res, condition):
    if protocal.FUNCTION_TYPE_CALLABLE in condition:
        condition = utils.string_to_function(condition[FUNCTION_TYPE_CALLABLE], "condition")
    elif protocal.FUNCTION_TYPE_DEFAULT in condition:
        if condition[FUNCTION_TYPE_DEFAULT] == default_condition.CONDITION_CLOCK_TICK:
            __clock_tick_event_receiver.append(event_id)
            return
        else:
            condition = default_condition.get_condition(condition[FUNCTION_TYPE_DEFAULT])
    else:
        raise Exception("unknown condition:" + condition)
    res_manager.add_listener(ref_res, condition, lambda: sky_client.write(tuple=(RECEIVER, "Event", event_id)))


# func_name-->function.
def init_remote_call_book():
    global remote_call_book
    remote_call_book = dict()
    remote_call_book["add_res"] = handle_add_res
    remote_call_book["modify_res_value"] = res_manager.modify_value
    remote_call_book["set_res_value"] = res_manager.set_res_value
    remote_call_book["get_res_value"] = res_manager.get
    remote_call_book["get_res_values"] = res_manager.get_all
    remote_call_book["update_res"] = res_manager.update
    remote_call_book["get_clock"] = Clock.get
    remote_call_book["ticktock"] = handle_ticktock
    remote_call_book["reset_res_pool"] = reset
    remote_call_book["add_event_listener"] = handle_add_event_listener


def __res_server__():
    # template (TARGET, func_name, paramter, content_id)
    template = (TARGET, "?", "?", "?")
    while True:
        try:
            request, request_id = sky_client.take(template, return_id=True, timeout=60000)
            if request is None:
                continue

            _, func_name, param = request
            param = utils.decode(param)
            log().info("REQUEST, func_name=%s, params=%s", func_name, param)

            if func_name in remote_call_book:
                function = remote_call_book[func_name]
                result = function(**param)
                log().info("Result=%s", str(result))
                sky_client.write(tuple=(RECEIVER, request_id, utils.encode(result)), expire=3000)
            else:
                log().warn("invalid func_name:%s", func_name)
        except Exception as e:
            log().error("handle request error, exception:%s\n%s", e, traceback.format_exc())


# __server_thread__ = threading.Thread(target=__res_server__)


def start():
    # __server_thread__.start()
    reset()
    __res_server__()


__clock_tick_event_receiver = list()
__on_tick = False




@utils.timing
def tick_or_tock():
    global __on_tick
    if not __on_tick:
        res_manager.changed_res_set.clear()
        res_manager.run_timer()
        __on_tick = True
        if len(__clock_tick_event_receiver) > 0:
            for receiver in __clock_tick_event_receiver:
                notify_id = sky_client.write((RECEIVER, "Event", receiver),fill_content_id=True)
                #sky_client.take(template=(TARGET, notify_id, '?'))
    else:
        res_manager.run_listener()
        Clock.tick()
        report()
        __on_tick = False


def report():
    print "-----------------------------------------------------"
    print "CLOCK:", Clock.get()
    res_manager.report()
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"


def init_log():
    import logging.config

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,  # this fixes the problem

        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    })


if __name__ == "__main__":
    init_log()
    init_remote_call_book()
    start()
    print "started"