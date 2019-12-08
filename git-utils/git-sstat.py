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
from argparse import ArgumentParser
from pathlib import Path


VERSION = "0.2.0"


def main():
    """Get filtered short status of current directory"""
    args = ["git", "status", "-s", "-b"]
    finished_proc = subprocess.run(args, capture_output=True)
    if finished_proc.returncode == 128:
        print(f"{os.getcwd()}: Not a git repo")
        return
    status = finished_proc.stdout
    if b"ahead" in status or b"behind" in status or status.count(b"\n") > 1:
        p = Path(".").resolve()
        print("/".join(p.parts[-2:]))
        print(status.decode())


if __name__ == "__main__":
    p = ArgumentParser(prog="git-sstat")
    p.add_argument("-v", "--version", action="store_true")
    args = p.parse_args()

    if args.version:
        print(Path(__file__).stem, VERSION)
    else:
        sys.exit(main())
