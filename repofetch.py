#!/usr/bin/env python
import multiprocessing
import os
import subprocess
from pathlib import Path


def fetch(direc):
    print(direc)
    finished = subprocess.run(["git", "fetch", "--all"], capture_output=True, cwd=direc)
    output = finished.stdout.decode()
    if output == "Fetching origin\n":
        return None
    return f"{str(direc)}\n\t{output}"


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
