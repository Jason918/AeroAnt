from ResPool.clock import Clock
from res_manager import *

__author__ = 'jason'
import client
from random import random


client.ticktock(1)
print client.get_clock()
temp = "temperature"


def update(value, delta):
    print type(value)
    print type(delta)
    return value + delta


client.add_res(temp, 20, update)


def humidity_update(value):
    if Clock.get() % 2 == 0:
        return value + random() * 0.1
    else:
        return value - random() * 0.1


hum = "humidity"
client.add_res(hum, 0.5, humidity_update)

sen = "sensor"
client.add_res(sen, {'humidity': 0.5, 'temperature': 20},
               lambda: {'humidity': get('humidity'), 'temperature': get('temperature')})

client.ticktock(1)
client.update_res(temp, 2, 3)
client.update_res(hum, 1)
client.update_res(sen, 1)
client.ticktock(10)

print client.get_res_value(temp)
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
