#!/usr/bin/env python3
import os
import subprocess
from multiprocessing import Pool


def get_status(path):
    os.chdir(path)
    output = subprocess.run(
        ["git", "status", "-s", "-b"], stdout=subprocess.PIPE
    ).stdout.decode(encoding="UTF-8")
    return path, output.split("\n")


def main():
    repo_dir = os.path.expanduser("~/devel")
    contents = [os.path.join(repo_dir, f) for f in os.listdir(repo_dir)]
    repos = [f for f in contents if os.path.isdir(f)]
    curdir = os.getcwd()
    pool = Pool()
    outputs = pool.map(get_status, repos)
    os.chdir(curdir)
    curdir = os.getcwd()
    fat_statuses = [(path, status) for (path, status) in outputs if len(status) > 2]
    for path, status in sorted(fat_statuses):
        print(path)
        print("=" * len(path))
        for line in status:
            print(line)


if __name__ == "__main__":
    main()
