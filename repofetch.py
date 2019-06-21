#!/usr/bin/env python
import multiprocessing
import os
import subprocess
from pathlib import Path


def fetch(direc):
    if not direc.is_dir():
        return None
    if not (direc / ".git").exists():
        return None
    finished = subprocess.run(["git", "fetch", "--all"], capture_output=True, cwd=direc)
    output = finished.stdout.decode()
    if output == "Fetching origin\n":
        return None
    return f"{str(direc)}\n\t{output}"


if __name__ == "__main__":
    dirs = [
        d
        for d in Path(os.environ["CODEDIR"]).resolve().glob("*")
        if d.is_dir() and (d / ".git").exists()
    ]
    for result in multiprocessing.Pool().imap(fetch, dirs):
        if result:
            print(result)
            print()
