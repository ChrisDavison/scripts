#!/usr/bin/env python3
import subprocess
from pathlib import Path


def git_output(args, cwd):
    proc = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)
    return proc.stdout.decode().splitlines()


def branchstat(path):
    statuses = [ahead_behind(path), modified(path), status(path), untracked(path)]
    print(", ".join([s for s in statuses if s]))


def ahead_behind(path):
    out = git_output(
        [
            "for-each-ref",
            "--format='%(refname:short) %(upstream:track)'",
            "refs/heads",
        ],
        path,
    )
    tidy_out = []
    for line in out:
        tidy = line.strip("'").split(" ")
        if len(tidy) > 1 and tidy[1]:
            tidy_out.append(" ".join(tidy))
    return "".join(tidy_out)


def modified(path):
    out = " ".join(git_output(["diff", "--shortstat"], path))
    if "changed" in out:
        return f"Modified {out.split(' ')[1].strip()}"
    return None


def status(path):
    out = git_output(["diff", "--stat", "--cached"], path)
    if out:
        return f"Staged {len(out)}"
    return None


def untracked(path):
    out = git_output(["ls-files", "--others", "--exclude-standard"], path)
    if out:
        return f"Untracked {len(out)}"
    return None


branchstat(Path("."))
