__author__ = 'jason'
import client
from random import random


client.ticktock(1)
print client.get_clock()
# temp = "temperature"
# client.add_res(temp, "20", lambda value, delta: value + delta)


# def humidity_update(value):
# if Clock.get() % 2 == 0:
#         return value + random() * 0.1
#     else:
#         return value - random() * 0.1


# hum = "humidity"
# add(hum, "0.5", humidity_update)
#
# sen = "sensor"
# add(sen, "{'humidity':0.5,'temperature':20}", lambda: {'humidity': get('humidity'), 'temperature': get('temperature')})
# tick()
# tock()
#
# tick()
# update(temp, 2, 3)
# update(hum, 1)
# update(sen, 1)


# def alert():
#     print "WARNING!!!!!!temp=", get(temp), "humidity:", get(hum)
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
