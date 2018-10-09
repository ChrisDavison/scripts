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


def fetch(repo):
    """Fetch all repos."""

    def filtered(status):
        """Filter only repos that have fetched something"""
        return [
            line
            for line in status.split("\n")
            if not line.startswith("Fetching") and not line == ""
        ]
    os.chdir(repo)
    out = subprocess.run(
        ["git", "fetch", "--all"], stdout=subprocess.PIPE
    ).stdout.decode(encoding="UTF-8")
    return repo, filtered(out)


def stat(repo):
    """Get long status of current branch."""

    def filtered(status):
        """Filter only branches with changes"""
        return status if len(status.split("\n")) > 2 else None

    os.chdir(repo)
    output = subprocess.run(
        ["git", "status", "-s", "-b"], stdout=subprocess.PIPE
    ).stdout.decode(encoding="UTF-8")
    return repo, filtered(output)


def bstat(repo):
    """Get short status of all branches."""

    def filtered(status):
        """Filter only branches not up to date"""
        for word in ["ahead", "behind", "modified", "untracked"]:
            if word in status:
                return status
        return None

    os.chdir(repo)
    output = subprocess.run(
        ["git", "branchstat"], stdout=subprocess.PIPE
    ).stdout.decode(encoding="UTF-8")
    return repo, filtered(output)


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
    repo_functions = {"fetch": fetch, "stat": stat, "bstat": bstat}
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
