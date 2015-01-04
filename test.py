import logging.config
from time import sleep
from ResPool import default_condition

__author__ = 'jason'

import ResPool.client as c

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,  # this fixes the problem

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
            'level': 'INFO',
            'propagate': True
        }
    }
})


def action():
    print "hahahaha.....@", c.get_clock()


c.init_listener()

c.register_listener([], default_condition.CONDITION_CLOCK_TICK, action)

while True:
    sleep(5)