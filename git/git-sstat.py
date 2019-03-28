#!/usr/bin/env python3
"""
usage: git-branchstat [-v|-h]

options:
    -v     Show version
    -h     Show this message
"""
import os
import subprocess
import sys
from pathlib import Path

from docopt import docopt


VERSION = "0.2.0"


def git(*args):
    return subprocess.run(['git'] + list(args), capture_output=True)


def main():
    finished_proc = git('status', '-s', '-b')
    if finished_proc.returncode == 128:
        print("Not a git repo")
        return
    status = finished_proc.stdout
    if b'ahead' in status or b'behind' in status or status.count(b'\n') > 1:
        p = Path('.').resolve()
        print('/'.join(p.parts[-2:]))
        print(status.decode())
    

if __name__ == "__main__":
    args = docopt(__doc__)
    if args['-v']:
        print(Path(__file__).stem, VERSION)
        sys.exit(0)
    sys.exit(main())

