#!/usr/bin/env python3
import multiprocessing
import os
import subprocess
from pathlib import Path


def fetch(direc):
    if not direc.is_dir():
        return None
    if not (direc / ".git").exists():
        return None
    finished = subprocess.run(["git", "sstat"], capture_output=True, cwd=direc)
    output = finished.stdout.decode().strip()
    if output:
        return f"{output}"
    return None


if __name__ == "__main__":
    dirs = [d for d in Path(os.environ["CODEDIR"]).resolve().glob("*")]
    for result in multiprocessing.Pool().imap(fetch, dirs):
        if result:
            print(result)
            print()
