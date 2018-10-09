#!/usr/bin/env python3
"""Repo utils.

Run repo functions across multiple repos in parallel.

Usage:
    repo fetch|stat|bstat

Commands:
    fetch   Fetch all repos
    stat    Show long status of current branch
    bstat   Show short branch status of all branches
"""
import os
import subprocess
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
    return repo, filtered


def stat(repo):
    """Get long status of current branch, only showing if unclean."""
    os.chdir(repo)
    output = run_on_git("status", "-s", "-b")
    filtered = output if len(output.split("\n")) > 2 else None
    return repo, filtered


def bstat(repo):
    """Get short status of all branches, only showing if unclean."""
    os.chdir(repo)
    output = run_on_git("branchstat")
    filtered = None
    for word in ["ahead", "behind", "modified", "untracked"]:
        if word in output:
            filtered = output
            break
    return repo, filtered


def for_each_repo(repos, function):
    """Run a function across every repo."""
    outputs = Pool().map(function, repos)
    for path, status in sorted(outputs):
        if status:
            print(os.path.basename(path))
            print("=" * len(os.path.basename(path)))
            print(status)


def main():
    """Run a function under all repos in ~/devel."""
    args = docopt(__doc__)
    repo_functions = { "fetch": fetch, "stat": stat, "bstat": bstat }
    commands = [command for command, status in args.items() if status]
    assert (
        len(commands) == 1
    ), f"Ambiguous command.  Must be one of {repo_functions.keys()}"
    function = repo_functions[commands[0]]
    repo_dir = os.path.expanduser("~/devel")
    contents = [os.path.join(repo_dir, f) for f in os.listdir(repo_dir)]
    repos = [f for f in contents if os.path.isdir(f)]
    curdir = os.getcwd()
    for_each_repo(repos, function)
    os.chdir(curdir)


if __name__ == "__main__":
    main()
