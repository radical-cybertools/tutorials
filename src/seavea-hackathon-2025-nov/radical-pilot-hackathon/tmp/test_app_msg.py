#!/usr/bin/env python3

import radical.pilot as rp


if __name__ == '__main__':

    session = rp.Session()
    try:

        pmgr  = rp.PilotManager(session=session)
        tmgr  = rp.TaskManager(session=session)
        pdesc = rp.PilotDescription({'resource': 'local.localhost',
                                     'runtime' : 60,
                                     'nodes'   : 3})
        pilot = pmgr.submit_pilots(pdesc)
        tmgr.add_pilots(pilot)

        tds = list()
        for i in range(2):
            td = rp.TaskDescription({'executable': '/home/merzky/j/rp/msg_client.py',
                                     'named_env' : 'rp'})
            tds.append(td)

        tasks = tmgr.submit_tasks(tds)

        tmgr.wait_tasks(uids=[task.uid for task in tasks])

        for task in tasks:
            print('STDERR: %s' % task.stderr)
            print('STDOUT: %s' % task.stdout)

    finally:
        session.close(download=True)


# ------------------------------------------------------------------------------

