#!/usr/bin/env python

import sys

DEBUG = False

def dbg(msg):
    global DEBUG
    if DEBUG:
        print msg
        sys.stdout.flush()