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
    cfg     = ru.Config(from_dict={'uid'      : channel,
                                   'channel'  : channel,
                                   'kind'     : 'pubsub',
                                   'log_level': 'debug_9',
                                   'path'     : os.getcwd(),
                                   'sid'      : 'rp.session.1',
                                   'bulk_size': 0,
                                   'stall_hwm': 1})

    b = ru.zmq.Bridge.create(channel, cfg=cfg)
    b.start()

    url_sub = str(b.addr_sub)
    url_pub = str(b.addr_pub)

    time.sleep(1)

    def sub_cb(topic, msg):
        print('=== sub: %s' % msg)

    subscriber = ru.zmq.Subscriber(channel=channel, topic=topic, cb=sub_cb, url=url_sub)
    subscriber.subscribe(channel)

    time.sleep(1)

    pub = ru.zmq.Publisher(channel=channel, url=url_pub)

    msg = {'cmd': 'testme'}
    pub.put(topic=topic, msg=msg)
    print('=== pub %s' % msg)

    time.sleep(3)

# ------------------------------------------------------------------------------
# run tests if called directly
if __name__ == '__main__':

    test_zmq_pubsub()


