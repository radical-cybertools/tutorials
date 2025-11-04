#c!/usr/bin/env python3

import os
import sys
import time
import ollama

import radical.utils as ru
import threading     as mt


def print(msg):
    sys.stdout.write('%.2f %s\n' % (time.time(), msg))
    sys.stdout.flush()


n_threads  = int(sys.argv[1])
n_requests = int(sys.argv[2])

prof = ru.Profiler('radical.ollama')
url  = os.environ.get('RP_INFO_LOAD_BALANCER')

assert url, 'load balancer url not set'
print('url: %s' % url)


# ------------------------------------------------------------------------------
#
def work(tid):

    print('start thread %s' % tid)

    client = ollama.Client(host=url)
    prompt = {'role'   : 'user',
              'stream' : False,
              'content': 'echo "Hello, World!"'}
    model  = 'gw2:0.5b'

    print('thread client: %s [%s]' % (client, url))

    # run one probe request to load the model
    try:
        for i in range(n_requests):
            print('req %d' % i)
            prof.prof('request_start', uid=tid, msg='request_%06d' % i)
            client.chat(model=model, messages=[prompt])
            prof.prof('request_stop', uid=tid, msg='request_%06d' % i)

    except Exception as e:
        print('ERROR: %s\n' % e)


# ------------------------------------------------------------------------------
#
def main():

    threads = list()

    for n in range(n_threads):
        tid = 'thread_%03d' % n

        prof.prof('threads_start', uid=tid)
        t = mt.Thread(target=work, args=[tid])
        t.daemon = True
        t.start()
        threads.append(t)

    print('threads started')

    for t in threads:
        t.join()

    print('threads joined')


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    main()


# ------------------------------------------------------------------------------

