#!/usr/bin/env python
import subprocess
import sys


VERSION = "0.2.0"


def main():
    args = sys.argv[1:]
    if args and args[0] == "version":
        print(f"git-branchstat {VERSION}")
        sys.exit(1)
    if not is_git_repo():
        print("Not a git repo.")
        sys.exit(1)
    outputs = [get_ahead_behind(), get_modified(), get_status(), get_untracked()]
    valid = [o for o in outputs if o]
    print(", ".join(valid))


def get_ahead_behind():
    finished = subprocess.run(
        [
            "git",
            "for-each-ref",
            "--format='%(refname:short) %(upstream:track)'",
            "refs/heads",
        ],
        capture_output=True,
    )
    if finished.returncode > 0:
        raise Exception("AheadBehind err: %s" % finished.stderr)
    changed = []
    for line in finished.stdout.split(b"\n"):
        tidy = line.decode("utf-8").strip("'\" ")
        if len(tidy.split(" ")) > 1:
            changed.append(tidy)
    return ", ".join(tidy)


def get_modified():
    finished = subprocess.run(["git", "diff", "--shortstat"], capture_output=True)
    if finished.returncode > 0:
        raise Exception("Modified err: %s" % finished.stderr)
    response = finished.stdout.decode("utf-8").strip("\n")
    if "file changed" in response:
        num = response.lstrip(" ").split(" ")[0]
        return f"Modified {num}"
    return None


def get_status():
    finished = subprocess.run(
        ["git", "diff", "--stat", "--cached"], capture_output=True
    )
    if finished.returncode > 0:
        raise Exception("Status err: %s" % finished.stderr)
    response = finished.stdout.split(b"\n")
    if response != [b""]:
        return f"Staged {len(response)}"
    return None


def get_untracked():
    finished = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"], capture_output=True
    )
    if finished.returncode > 0:
        raise Exception("Untracked err: %s" % finished.stderr)
    response = finished.stdout.split(b"\n")
    if response != [b""]:
        return f"Untracked {len(response)}"
    return None


def is_git_repo():
    finished = subprocess.run(["git", "branch"], capture_output=True)
    return finished.returncode != 128


if __name__ == "__main__":
    main()
