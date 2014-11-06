__author__ = 'jason'

import res_manager
from clock import Clock
import threading
import sky_client


def __res_server__():
    request_content = sky_client.get_content(["res_pool", "?", "?"])
    while True:
        request, rid = sky_client.take(request_content, return_id=True)
        func, param = request[1:2]
        res_value = None
        print "func=", func, "param=", param
        if func == "get_res":
            name, clock = param
            res_value = res_manager.get(name, clock)
        elif func == "add_res":
            name, model, update = param
            res_value = res_manager.add(name, model, update)
        elif func == "get_clock":
            res_value = Clock.get()
        elif func == "update_res":
            name, cycle, par = param
            res_value = res_manager.update(name, cycle, par)
        elif func == "add_listener":
            ref_res, condition, action = param
            res_manager.add_listener(ref_res, condition, action)
        elif func == "ticktock":
            time = int(param)
            for i in range(time):
                tick()
                tock()
        else:
            print "unknown function:", func
            continue
        result = sky_client.get_content(["res_pool_client", func, rid, res_value])
        sky_client.write(result, expire=3000)


__server_thread__ = threading.Thread(target=__res_server__)


def start():
    __server_thread__.start()


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


if __name__ == "__main__":
    start()
    print "started"