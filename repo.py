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
import sys
import subprocess
import contextlib
from dataclasses import dataclass
from multiprocessing import Pool
from docopt import docopt


@dataclass
class GitOutput:
    """GitOutput represents the output of a command ran on a repo."""
    repo: str = None
    status: str = None
    path_width: int = 1
    status_width: int = 1
    def __str__(self):
        """Return string representation of a Git command output"""
        return f"{self.repo}\n{self.status}\n"

    def set_padding(self, *, path, status):
        """Set padding for outputs"""
        self.path_width = path
        self.status_width = status


@dataclass
class GitBstatOutput(GitOutput):
    """GitBstatOutput represents the output of a branchstat command ran on a repo."""
    def __str__(self):
        """Overload the __str__ function to provide inline output."""
        return f"{self.repo:{self.path_width}} | {self.status:{self.status_width}} |"


@contextlib.contextmanager
def working_directory(path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.

    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(prev_cwd)


def run_on_git(*args):
    """Run a git subprocess with the given args"""
    git_args = ["git"]
    git_args.extend(args)
    return subprocess.run(git_args, stdout=subprocess.PIPE).stdout.decode(
        encoding="UTF-8"
    )


def fetch(repo):
    """Fetch all repos, showing only if something has fetched."""
    os.chdir(repo)
    output = run_on_git("fetch", "--all")
    filtered = [
        line
        for line in output.split("\n")
        if not line.startswith("Fetching") and not line == ""
    ]
    return GitOutput(os.path.basename(repo), filtered.strip())


def stat(repo):
    """Get long status of current branch, only showing if unclean."""
    os.chdir(repo)
    output = run_on_git("status", "-s", "-b")
    if len(output.split("\n")) > 2:
        return GitOutput(repo, output.strip())
    return GitOutput()


def bstat(repo):
    """Get short status of all branches, only showing if unclean."""
    os.chdir(repo)
    output = run_on_git("branchstat")
    for word in ["ahead", "behind", "modified", "untracked"]:
        if word in output:
            return GitBstatOutput(os.path.basename(repo), output.strip())
    return GitBstatOutput()


def is_git_repo(path):
    """Check if a path is a directory AND contains a .git subdir."""
    return os.path.isdir(path) and os.path.exists(os.path.join(path, ".git"))


def main():
    """Run a function under all repos in ~/devel."""
    args = docopt(__doc__)
    commands = {
        "fetch": fetch,
        "bstat": bstat,
        "stat": stat,
    }
    if args["<command>"] not in commands.keys():
        print(f"Invalid command `{args['<command>']}`\n")
        print(__doc__)
        sys.exit(1)
    command = commands[args["<command>"]]
    with working_directory(os.path.expanduser("~/devel")):
        repos = [os.path.join(os.getcwd(), f) for f in os.listdir() if is_git_repo(f)]
        outputs = Pool().map(command, repos)
        with_status = list(filter(lambda x: x.status, outputs))
        longest_path, longest_stat = 1, 1
        for output in with_status:
            if len(output.repo) > longest_path:
                longest_path = len(output.repo)
            if len(output.status) > longest_stat:
                longest_stat = len(output.status)
        for output in sorted(with_status, key=lambda x: x.repo):
            output.set_padding(path=longest_path, status=longest_stat)
            print(output)


if __name__ == "__main__":
    sys.exit(main())
