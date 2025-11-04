#!/usr/bin/env python3

import os
import time

import threading as mt

import radical.utils as ru


# ------------------------------------------------------------------------------
#
def test_zmq_pubsub():

    channel = 'control_pubsub'
    topic   = 'topic'

    b = ru.zmq.PubSub(channel)
    b.start()

    url_sub = str(b.addr_out)
    url_pub = str(b.addr_in)

    def cb(topic, msg):
        print(topic, msg)
        if msg['idx'] is None:
            return False

    ru.zmq.Subscriber(channel=channel, url=url_sub,
                      topic=topic, cb=cb)
    time.sleep(0.1)

    pub = ru.zmq.Publisher(channel=channel, url=url_pub)
    pub.put(topic, {'src': 'uid',
                    'idx': 'test'})

    time.sleep(0.1)

    b.stop()
    time.sleep(0.1)


# ------------------------------------------------------------------------------
# run tests if called directly
if __name__ == '__main__':

    test_zmq_pubsub()


