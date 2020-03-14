#!/usr/bin/env python
from argparse import ArgumentParser
from datetime import datetime, timedelta
import time

def time_as_hms(t):
    return datetime.now().strftime("%H:%M:%S")

def linecleared_message(m):
    print('\r' + (' ' * 40) + '\r' + m, end='')


parser = ArgumentParser()
parser.add_argument('duration', help='Duration in minutes', type=float)
parser.add_argument('-n', '--note', help='Note on the timer')
args = parser.parse_args()

seconds = 0
start = datetime.now()
end = datetime.now() + timedelta(minutes=args.duration)
note = (' ' + args.note + ' ') if args.note else ''
while datetime.now() < end:
    delta = (end - datetime.now()).total_seconds()
    delta_min = int(delta / 60)
    delta_seconds = int(delta - (delta_min * 60))
    msg = '{}{}m{}s'.format(note.lstrip(), delta_min, delta_seconds)
    linecleared_message(msg)
    time.sleep(1)
linecleared_message("Finished {}m{}!".format(args.duration, note.rstrip()))
print()
