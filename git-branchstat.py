#!/usr/bin/env python3
import subprocess


def get_branch_aheadbehind():
    """Identify ahead|behind status of all branches"""
    cmd = subprocess.run(
        [
            "git",
            "for-each-ref",
            '--format="%(HEAD) %(refname:short) %(upstream:track)"',
            "refs/heads",
        ],
        stdout=subprocess.PIPE,
    )
    decoded = cmd.stdout.decode(encoding="UTF-8")
    for line in decoded.split("\n"):
        print(line.strip().strip('"'))


def get_num_modified_and_untracked():
    """Count number of untracked and modified files in repo"""
    out = subprocess.run(
        ["git", "diff", "--stat"], stdout=subprocess.PIPE
    ).stdout.decode(encoding="UTF-8").strip()
    n_modified = len(out.split("\n")) - 1

    out = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"], stdout=subprocess.PIPE
    ).stdout.decode(encoding="UTF-8").strip()
    n_untracked = len(out.split("\n"))

    if n_untracked and n_modified:
        print(f"HEAD [modified {n_modified}, untracked {n_untracked}]")
    elif n_modified:
        print(f"HEAD [modified {n_modified}]")
    elif n_untracked:
        print(f"HEAD [untracked {n_untracked}]")
    else:
        return


if __name__ == "__main__":
    get_branch_aheadbehind()
    get_num_modified_and_untracked()
