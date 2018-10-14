#!/usr/bin/env python3
import subprocess


def get_branch_aheadbehind():
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


def get_num_modified_and_untracked():
    """Count number of untracked and modified files in repo"""
    out = (
        subprocess.run(["git", "diff", "--stat"], stdout=subprocess.PIPE)
        .stdout.decode(encoding="UTF-8")
        .strip()
    )
    n_modified = len(out.split("\n")) - 1

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

    if n_untracked and n_modified:
        return f"HEAD [modified {n_modified}, untracked {n_untracked}]"
    elif n_modified:
        return f"HEAD [modified {n_modified}]"
    elif n_untracked:
        return f"HEAD [untracked {n_untracked}]"
    else:
        return ""


if __name__ == "__main__":
    branchstat = get_branch_aheadbehind()
    modifiedstat = get_num_modified_and_untracked()
    if branchstat and modifiedstat:
        print(f"{modifiedstat}, {branchstat}")
    elif branchstat:
        print(f"{branchstat}")
    else:
        print(f"{modifiedstat}")
