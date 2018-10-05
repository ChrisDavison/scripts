#!/usr/bin/env python3
import os
import subprocess
from typing import List
from multiprocessing import Pool


def get_short_status(path):
    os.chdir(path)
    output = subprocess.run(
        ["git", "branchstat"], stdout=subprocess.PIPE
    ).stdout.decode(encoding="UTF-8")
    return path, output.split("\n")


def repo_has_changes(status: List[str]) -> bool:
    for word in ["ahead", "behind", "modified", "untracked"]:
        if word in "".join(status):
            return True
    return False


def main():
    repo_dir = os.path.expanduser("~/devel")
    contents = [os.path.join(repo_dir, f) for f in os.listdir(repo_dir)]
    repos = [f for f in contents if os.path.isdir(f)]
    curdir = os.getcwd()
    outputs = Pool().map(get_short_status, repos)
    modified = [
        (path, status) for (path, status) in outputs if repo_has_changes(status)
    ]
    for path, status in sorted(modified):
        print(os.path.basename(path))
        print("=" * len(os.path.basename(path)))
        for line in status:
            print(line)
    os.chdir(curdir)


if __name__ == "__main__":
    main()
