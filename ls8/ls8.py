# !/usr/bin/env python3

"""Main."""

import sys
from cpu import *
progname = sys.argv[1]

cpu = CPU()

cpu.load(progname)
cpu.run()