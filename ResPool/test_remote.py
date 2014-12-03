from time import sleep
from ResPool.clock import Clock
from res_manager import *

import default_functions

__author__ = 'jason'
import client
from random import random


client.reset_res_pool()


def test_xml_load():
    print "testing xml load"
    names = client.add_res_from_file("../res.xml")
    for i in range(1):
        client.ticktock(1)
        sleep(1)
        print
        print "clock:", client.get_clock()
        for name in names:
            print name, ":", client.get_res_value(name)


test_xml_load()


def test_old():
    client.ticktock(1)
    print client.get_clock()
    temp = "temperature"
    # def update(value, delta):
    # print type(value)
    # print type(delta)
    #     return value + delta
    update = {
        "method": default_functions.METHOD_RANDINT,
        "min": 11,
        "max": 20
    }
    client.add_res(temp, 20, update)
    # def humidity_update(value):
    #     if Clock.get() % 2 == 0:
    #         return value + random() * 0.1
    #     else:
    #         return value - random() * 0.1
    hum = "humidity"
    client.add_res(hum, "S1", {
        "method": default_functions.METHOD_MARKOV_CHAIN,
        "states": ["S1", "S2", "S3"],
        "transform": [
            [0.2, 0.5, 0.3],
            [0.2, 0.5, 0.3],
            [0.2, 0.5, 0.3],
        ]
    })

    sen = "sensor"
    client.add_res(sen, {'humidity': 0.5, 'temperature': 20}, {
        "method": default_functions.METHOD_TIME,
        "format": "%H%M%S"
    })
    # lambda: {'humidity': get('humidity'), 'temperature': get('temperature')})

    client.ticktock(1)
    client.update_res(temp, 2, 3)
    client.update_res(hum, 1)
    client.update_res(sen, 1)

    for i in range(100):
        client.ticktock(1)
        print "clock:", client.get_clock()
        print temp, ":", client.get_res_value(temp)
        print hum, ":", client.get_res_value(hum)
        print sen, ":", client.get_res_value(sen)
        print


        # def alert():
        # print "WARNING!!!!!!temp=", get(temp), "humidity:", get(hum)
        #
        #
        # lid = add_listener([temp, hum], lambda: get(temp) > 30 or get(hum) < 0.4, alert)
        # tock()
        #
        # for i in range(10):
        #     tick()
        #     tock()
        #
        # res_manager.report_xml()
