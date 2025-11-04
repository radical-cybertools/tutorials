#!/usr/bin/env python3

__copyright__ = 'Copyright 2013-2014, http://radical.rutgers.edu'
__license__   = 'MIT'

import radical.pilot as rp
import radical.utils as ru


# ------------------------------------------------------------------------------
#
# READ the RADICAL-Pilot documentation: https://radicalpilot.readthedocs.io/
#
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    # we use a reporter class for nicer output
    report = ru.Reporter(name='radical.pilot')
    report.title('Getting Started (RP version %s)' % rp.version)

    session = rp.Session()
    try:
        pmgr   = rp.PilotManager(session=session)
        tmgr   = rp.TaskManager(session=session)

        report.header('submit pilots')

        pd_init = {'resource'      : 'debug.flux_spack',
                   'runtime'       : 60,
                   'exit_on_error' : True,
                   'nodes'         : 5
                  }
        pdesc = rp.PilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)

        n = 1024  # number of tasks to run
        report.header('submit %d tasks' % n)

        tmgr.add_pilots(pilot)

        report.progress_tgt(n, label='create')
        tds = list()
        for i in range(n):

            # create a new task description, and fill it.
            td = rp.TaskDescription()
            td.executable = '/bin/sh'
            td.arguments = ['-c', 'echo $RP_TASK_ID $RP_PARTITION_ID $RP_PILOT_ID']

            tds.append(td)
            report.progress()

        report.progress_done()

        tasks = tmgr.submit_tasks(tds)

        tmgr.wait_tasks()

        for task in tasks:
            print('  * %s: %s [%s], %s' % (task.uid, task.state, task.exit_code,
                                           task.stdout.strip()))

    finally:
        report.header('finalize')
        session.close(download=True)

    report.header()


# ------------------------------------------------------------------------------

