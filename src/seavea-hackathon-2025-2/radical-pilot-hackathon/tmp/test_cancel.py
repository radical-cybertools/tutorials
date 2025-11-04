#!/usr/bin/env python3

import time

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
def state_cb(task, state):
    print('%.06f ==== %s: %s' % (time.time(), task.uid, state))


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    session = rp.Session()

    try:
        pmgr = rp.PilotManager(session=session)
        tmgr = rp.TaskManager(session=session)
        pd_init = {'resource'      : 'local.localhost',
                   'runtime'       : 1,
                   'exit_on_error' : True,
                   'nodes'         : 1,
                  }
        pdesc = rp.PilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)
        tmgr.add_pilots(pilot)
        tmgr.register_callback(state_cb)

        tds = list()
        for i in range(2):

            td = rp.TaskDescription()
            td.executable = '/bin/sh -c "sleep 30 ; false"'
            tds.append(td)

        tasks = tmgr.submit_tasks(tds)
        tmgr.wait_tasks(uids=[tasks[0].uid], state=[rp.AGENT_EXECUTING])

        for task in tasks:
            print('  * %s: %s' % (task.uid, task.state))

        tmgr.cancel_tasks([t.uid for t in tasks])
        tmgr.wait_tasks()

        for task in tasks:
            print('  * %s: %s [%s]' % (task.uid, task.state, task.exit_code))

    finally:
        session.close(download=True)


# ------------------------------------------------------------------------------

