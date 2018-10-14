#!/usr/bin/env python3
"""Get status of each git branch, as well as HEAD's modified and untracked status."""
import subprocess


def get_branches_aheadbehind_status():
    """Identify ahead|behind status of all branches"""
    cmd = subprocess.run(
        [
            "git",
            "for-each-ref",
            '--format="%(refname:short) %(upstream:track)"',
            "refs/heads",
        ],
        stdout=subprocess.PIPE,
    )
    decoded = cmd.stdout.decode(encoding="UTF-8").strip()
    branches_with_changes = []
    for line in decoded.split("\n"):
        tidied = line.strip('"').strip()
        if len(tidied.split(" ")) > 1:
            branches_with_changes.append(tidied)
    return ", ".join(branches_with_changes)


def get_modified_status():
    """Count number of modified files in repo."""
    out = (
        subprocess.run(["git", "diff", "--stat"], stdout=subprocess.PIPE)
        .stdout.decode(encoding="UTF-8")
        .strip()
    )
    n_modified = len(out.split("\n")) - 1
    if n_modified:
        return f"modified {n_modified}"
    return ""


def get_untracked_status():
    """Count number of untracked files in repo."""
    out = (
        subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            stdout=subprocess.PIPE,
        )
        .stdout.decode(encoding="UTF-8")
        .strip()
        .split("\n")
    )
    n_untracked = len(out) if out != [""] else 0
    if n_untracked:
        return f"untracked {n_untracked}"
    return ""


if __name__ == "__main__":
    print(", ".join([
        get_branches_aheadbehind_status(),
        get_modified_status(),
        get_untracked_status(),
    ]).strip(", "))
