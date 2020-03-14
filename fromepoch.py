#!/usr/bin/env python
import sys
import time

time_epoch = None
if len(sys.argv) > 1:
    time_epoch = sys.argv[1]
t = time.localtime(time_epoch)
print(time.strftime("%Y%m%d %H:%M:%S", t))
