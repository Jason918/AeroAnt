__author__ = 'jason'

import res_manager
import utils
from clock import Clock


def start():
    pass


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
