#!/usr/bin/env python3

import sys
import time

import radical.utils as ru
import threading     as mt


def work():
    for i in range(3):
        print('I am working...', i)
        time.sleep(1)
    print('work done')
    ru.cancel_main_thread()
    print('work done, really')
    raise RuntimeError('work failed')



t = mt.Thread(target=work)
t.daemon = True
t.start()

print('work thread started')
for j in range(10):
    print('I am waiting...', j)
    time.sleep(1)

print('main thread done')
