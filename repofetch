#!/usr/bin/env python3
import os
import subprocess
from multiprocessing import Pool


def fetch(repo):
    """Count number of untracked and modified files in repo"""
    os.chdir(repo)
    out = subprocess.run(
        ["git", "fetch", "--all"], stdout=subprocess.PIPE
    ).stdout.decode(encoding="UTF-8")
    return repo, out


def main():
    repo_dir = os.path.expanduser("~/devel")
    contents = [os.path.join(repo_dir, f) for f in os.listdir(repo_dir)]
    repos = [f for f in contents if os.path.isdir(f)]
    curdir = os.getcwd()
    outputs = Pool().map(fetch, repos)
    for path, status in sorted(outputs):
        has_non_fetch_line = [
            line
            for line in status.split("\n")
            if not line.startswith("Fetching") and not line == ""
        ]
        if has_non_fetch_line:
            print(os.path.basename(path))
            print("=" * len(os.path.basename(path)))
            print(status)
    os.chdir(curdir)


if __name__ == "__main__":
    main()
