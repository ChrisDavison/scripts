#!/usr/bin/env python3
"""Repo utils.

Run repo functions across multiple repos in parallel.

Usage:
    repo <command> [-h|--help]

Options:
    -h --help     Show this help message

Commands:
    fetch   Fetch all repos
    stat    Show long status of current branch
    bstat   Show short branch status of all branches
"""
import os
import subprocess
from collections import namedtuple
from multiprocessing import Pool
from docopt import docopt


def run_on_git(*args):
    """Run a git subprocess with the given args"""
    git_args = ["git"]
    git_args.extend(args)
    return subprocess.run(git_args, stdout=subprocess.PIPE
    ).stdout.decode(encoding="UTF-8") 


def fetch(repo):
    """Fetch all repos, showing only if something has fetched."""
    os.chdir(repo)
    output = run_on_git("fetch", "--all")
    filtered = [
        line
        for line in output.split("\n")
        if not line.startswith("Fetching") and not line == ""
    ]
    return os.path.basename(repo), filtered


def stat(repo):
    """Get long status of current branch, only showing if unclean."""
    os.chdir(repo)
    output = run_on_git("status", "-s", "-b")
    filtered = output if len(output.split("\n")) > 2 else None
    return os.path.basename(repo), filtered


def bstat(repo):
    """Get short status of all branches, only showing if unclean."""
    os.chdir(repo)
    output = run_on_git("branchstat")
    for word in ["ahead", "behind", "modified", "untracked"]:
        if word in output:
            return os.path.basename(repo), output
    return None, None


def is_git_repo(path):
    """Check if a path is a directory AND contains a .git subdir."""
    return os.path.isdir(path) and os.path.exists(os.path.join(path, ".git"))


def main():
    """Run a function under all repos in ~/devel."""
    args = docopt(__doc__)
    Command = namedtuple("Command", ["function", "short"])
    command = {
        "fetch": Command(function=fetch, short=False),
        "bstat": Command(function=bstat, short=True),
        "stat": Command(function=stat, short=False)
    }[args["<command>"]]
    curdir = os.getcwd()
    os.chdir(os.path.expanduser("~/devel"))
    repos = [os.path.join(os.getcwd(), f) for f in os.listdir() if is_git_repo(f)]
    outputs = Pool().map(command.function, repos)
    with_status = list(filter(lambda x: x[1], outputs))
    path_lens = list(map(lambda output: len(output[0]), with_status))
    stat_lens = list(map(lambda output: len(output[1]), with_status))
    longest_path = max(path_lens) if path_lens else 1
    longest_stat = max(stat_lens)-1 if stat_lens and command.short else 1
    # If we want short output, replace newline with pipe (i.e. shunt status right)
    spacing = " | " if command.short else "\n"
    for path, status in sorted(with_status):
        print(f"{path:{longest_path}}{spacing}{status.strip():{longest_stat}}{spacing}")
    os.chdir(curdir)


if __name__ == "__main__":
    main()
