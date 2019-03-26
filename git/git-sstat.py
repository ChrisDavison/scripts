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


version = "0.2.0"


def isGitRepo(path):
    return False


def git(*args):
    return subprocess.check_output(['git'] + list(args))


def main():
    status = git('status', '-s', '-b')
    if b'ahead' in status or b'behind' in status or status.count(b'\n') > 1:
        p = Path('.').resolve()
        print('/'.join(p.parts[-2:]))
        print(status.decode())
    

if __name__ == "__main__":
    sys.exit(main())
