#!/usr/bin/env python3

import os
import radical.utils as ru

import radical.saga.utils.misc as rsum
import radical.saga.filesystem as rsfs

def copy(src, tgt, flags):

  # if rsum.url_is_local(src): src = src.path
  # if rsum.url_is_local(tgt): tgt = tgt.path

    tmp      = ru.Url(tgt)
    tmp.path = '/'

    fs     = rsfs.Directory(str(tmp))
    flags |= rsfs.CREATE_PARENTS

    if os.path.isdir(src.path) or src.path.endswith('/'):
        print("===== isdir %s" % src.path)
      # flags |= rsfs.RECURSIVE

    print("===== copy %s -> %s [%s]" % (src, tgt, flags))
    fs.copy(str(src), tgt, flags=flags)

src = ru.Url('file:///tmp/FOO')
tgt = ru.Url('sftp://95.217.193.116/tmp/pilot.0000//foo')

copy(src, tgt, 0)

src = ru.Url('file:///tmp/BAR')
tgt = ru.Url('sftp://95.217.193.116/tmp/pilot.0000//bar')

copy(src, tgt, 0)

