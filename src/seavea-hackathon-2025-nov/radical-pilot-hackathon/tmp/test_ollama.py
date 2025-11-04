#!/usr/bin/env python3

import sys
import time

import radical.pilot as rp

BASE   = '/home/merzky/j/ollama'

OLLAMA = '%s/ollama'                % BASE
CLIENT = '%s/test_ollama_client.py' % BASE

N_NODES                   =  1
OLLAMAS_PER_NODE          =  1
OLLAMA_GPUS_PER_RANK      =  1

CLIENTS_PER_NODE          =  1
CLIENT_RANKS_PER_NODE     =  1
CLIENT_THREADS_PER_RANK   =  1
CLIENT_PROMPTS_PER_THREAD = 10


# ------------------------------------------------------------------------------
#
def print(msg):
    sys.stdout.write('%.2f %s\n' % (time.time(), msg))
    sys.stdout.flush()


if __name__ == '__main__':

    session = rp.Session()
    try:
        pmgr  = rp.PilotManager(session=session)
        tmgr  = rp.TaskManager(session=session)
        pdesc = rp.PilotDescription({'resource': 'local.localhost',
                                     'runtime' : 1024 * 1024,
                                     'nodes'   : N_NODES})
        pilot = pmgr.submit_pilots(pdesc)
        tmgr.add_pilots(pilot)

        # ---------------------------------------------------------------------
        # prepare the OLLAMA environment
      # pilot.prepare_env('ollama_env', {'type'    : 'venv',
      #                                  'path'    : '/tmp/ve_ollama',
      #                                  'setup'   : ['ollama', 'radical.pilot',
      #                                               '/home/merzky/j/rp'],
      #                                 })

        # ---------------------------------------------------------------------
        # start OLLAMA instances
        # ollama instances need ports assigned manually
        ods = list()
        for i in range(N_NODES * OLLAMAS_PER_NODE):
            getip = 'python3 -c "import radical.utils as ru; print(ru.get_hostip())"'
            port  = 11000 + i
            pat   = '.*Listening on ([0-9:\\.]*).*'
            od    = rp.TaskDescription(
                    {'uid'          : 'ollama_%04d' % i,
                     'mode'         : rp.TASK_SERVICE,
                     'executable'   : OLLAMA,
                     'arguments'    : ['serve'],
                     'gpus_per_rank': OLLAMA_GPUS_PER_RANK,
                     'pre_exec'     : [
                         'hostip=$(%s)' % getip,
                         'export OLLAMA_HOST=$hostip:%d' % port,
                         'echo RP_TASK_ID:$RP_RANK:$OLLAMA_HOST'],
                     'info_pattern' : 'stderr:%s' % pat,
                     'timeout'      : 10,  # startup timeout
                     'named_env'    : 'rp'})
            ods.append(od)

        ollamas = tmgr.submit_tasks(ods)

        # collect the endpoint URLs
        urls    = list()
        for ollama in ollamas:
            info = ollama.wait_info()
            print('found %s: %s' % (ollama.uid, info))
            urls.extend(list(info.values()))

        print('ollama urls: %s' % urls)

        # ---------------------------------------------------------------------
        # start the load balancer
        pat = 'Running on (.*)'
        td = rp.TaskDescription({'uid'         : 'load_balancer',
                                 'mode'        : rp.TASK_SERVICE,
                                 'executable'  : 'radical-pilot-http-balancer',
                                 'arguments'   : urls,
                                 'info_pattern': 'stderr:%s' % pat,
                                 'timeout'     : 10,
                                 'named_env'   : 'rp'})
        balancer = tmgr.submit_tasks(td)
        print('%s %s' % (balancer.uid, balancer.wait_info()))

        # ---------------------------------------------------------------------
        # start the clients (uses `load_balancer` service env)
        tds = list()
        for _ in range(CLIENTS_PER_NODE * N_NODES):
            td  = rp.TaskDescription({'executable' : CLIENT,
                                      'services'   : [balancer.uid],
                                      'ranks'      : CLIENT_RANKS_PER_NODE,
                                      'arguments'  : [CLIENT_THREADS_PER_RANK,
                                                      CLIENT_PROMPTS_PER_THREAD],
                                      'named_env'  : 'rp'})
            tds.append(td)

        tasks = tmgr.submit_tasks(tds)
        tmgr.wait_tasks(uids=[t.uid for t in tasks])

        # ---------------------------------------------------------------------
        # print some stats
        for task in tasks:
            print('STDOUT: %s' % task.stdout)
            print('STDERR: %s' % task.stderr)

    finally:
        session.close(download=True)


# ------------------------------------------------------------------------------

