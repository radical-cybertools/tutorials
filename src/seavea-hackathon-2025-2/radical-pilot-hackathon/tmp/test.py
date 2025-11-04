#!/usr/bin/env python3

import sys
print('version ', sys.version)

raise_all = False

try:
    import cffi
    print('cffi ok ', cffi.__file__)
except ImportError:
    print('cffi nok')
    if raise_all: raise

try:
    import flux
    print('flux ok ', flux.__file__)
except ImportError:
    print('flux nok')
    if raise_all: raise

try:
    import radical.gtod as rg
    print('rg   ok ', rg.__file__)
except ImportError:
    print('rg   nok')
    if raise_all: raise

try:
    import radical.pilot as rp
    print('rp   ok ', rp.__file__)
except ImportError:
    print('rp   nok')
    if raise_all: raise

