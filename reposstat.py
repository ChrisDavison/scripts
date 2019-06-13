#!/usr/bin/env python
import multiprocessing
import os
import subprocess
from pathlib import Path


def fetch(direc):
    os.chdir(direc)
    finished = subprocess.run(["git", "sstat"], capture_output=True)
    output = finished.stdout.decode().strip()
    if output:
        return f"{output}"
    return None


def main():
    codedir = os.environ['CODEDIR']
    dirs = [d for d in Path(codedir).resolve().glob('*')
            if d.is_dir() and (d / ".git").exists()]
    for result in multiprocessing.Pool().imap(fetch, dirs):
        if result:
            print(result)
            print()


if __name__ == "__main__":
    main()
