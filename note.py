#!/usr/bin/env python3
"""note - Modify or view NOTES file, or search notes directory.

Usage:
    note CMD [ARGS...]

Commands:
    a - add to NOTES file
    v - view full NOTES file
    e - edit NOTES file
    d - delete(empty) NOTES file
    f - find a note (optional: -f filename, -d directory, and/or -c contents)
    o - open files in vim
"""
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_NOTESFILE = Path("~/Dropbox/notes/inbox.md").expanduser()
NOTESFILE = Path(os.environ.get("NOTESFILE", DEFAULT_NOTESFILE))
NOTESDIR = Path(os.environ.get("NOTESDIR", NOTESFILE.parent))
EDITOR = os.environ.get("EDITOR", "nvim")
ALL_NOTES = NOTESDIR.rglob("*.txt")
ALL_NOTE_DIRS = [d for d in NOTESDIR.rglob("*") if d.is_dir()]

if not NOTESFILE.exists():
    NOTESFILE.touch()


def add(text):
    """Add whatever text is entered on the commandline to the NOTESFILE"""
    with NOTESFILE.open("a") as notes_file:
        print("\n{}\n".format(" ".join(text)), file=notes_file)


def find_matching_filenames(query):
    """Show files with filenames matching the given query"""
    print("===== MATCHING FILENAMES =====")
    for f in ALL_NOTES:
        if query in str(f):
            print(f.relative_to(NOTESDIR))


def find_matching_directories(query):
    """Show directories with name matching the given query"""
    print("===== MATCHING DIRECTORIES =====")
    for d in ALL_NOTE_DIRS:
        if query in str(d):
            print(d.relative_to(NOTESDIR))


def find_matching_file_contents(query):
    """Show files where contents matches the query"""
    print("===== MATCHING CONTENTS =====")
    if isinstance(query, list):
        query = " ".join(query)
    subprocess_args = ["rg", "-F", query, NOTESDIR, "-l", "--color=never"]
    output = subprocess.run(subprocess_args, stdout=subprocess.PIPE, check=True)
    for line in output.stdout.decode().split("\n"):
        if not line:
            continue
        fpath = Path(line).relative_to(NOTESDIR)
        print(fpath)


def tagfind(query):
    print("===== MATCHING ALL TAGS =====")
    if isinstance(query, list):
        query = " ".join(query)
    paths_matching_tags = set()
    for tag in query:
        paths_matching_this_tag = set()
        subprocess_args = ["rg", "-F", "@"+query, str(NOTESDIR), "-l", "--color=never"]
        output = subprocess.run(subprocess_args, stdout=subprocess.PIPE)
        for line in output.stdout.decode().split("\n"):
            if not line:
                continue
            paths_matching_this_tag.add(line) 
        if not paths_matching_tags:
            paths_matching_tags = paths_matching_this_tag
        else:
            paths_matching_tags &= paths_matching_this_tag
    for path in paths_matching_tags:
        fpath = Path(path).relative_to(NOTESDIR)
        print(fpath)

def find(args):
    """Find given query in filename, dirname, or file contents"""
    if not args:
        print("Must pass a query to find", file=sys.stderr)
        return
    find_files = "-f" in args
    find_dirs = "-d" in args
    find_contents = "-c" in args
    no_find_specified = not any([find_files, find_dirs, find_contents])

    print("Match is Filename, Directory, or Content")
    query = " ".join(args)
    if find_files or no_find_specified:
        find_matching_filenames(query)
    if find_dirs or no_find_specified:
        find_matching_directories(query)
    if find_contents or no_find_specified:
        find_matching_file_contents(query)


def view():
    """View contents of the NOTESFILE"""
    batstyle="--style=header,grid"
    subprocess.run(["bat", "-l", "md", batstyle, NOTESFILE], check=True)


def open_files(args):
    """Use FZF to select notes, with optional prefilter, then open in EDITOR"""
    query = " ".join(args)
    relative_files = "\n".join([str(n.relative_to(NOTESDIR)) for n in ALL_NOTES])
    subprocess_args = ["fzf", "-q", query, "--multi"]
    output = subprocess.run(
        subprocess_args,
        input=relative_files.encode(),
        check=True,
        stdout=subprocess.PIPE,
    )
    files = [NOTESDIR / f for f in output.stdout.decode().split("\n")]
    if not files:
        return None
    subprocess.run([EDITOR, *files], check=True)


def clear():
    """Erase the contents of NOTESFILE"""
    NOTESFILE.write_text("")


def edit():
    """Open NOTESFILE in EDITOR"""
    subprocess.run([EDITOR, NOTESFILE], check=True)


def main(*, command, args):
    """Dispatch the appropriate function based on CLI args"""
    if command in ["a", "add"]:
        add(args)
    elif command in ["f", "find"]:
        find(args)
    elif command in ["t", "tag"]:
        tagfind(args)
    elif command in ["tt", "tags"]:
        tagview(args)
    elif command in ["e", "edit"]:
        edit()
    elif command in ["v", "view"]:
        view()
    elif command in ["d", "delete", "del"]:
        clear()
    elif command in ["o", "open"]:
        open_files(args)
    else:
        print(__doc__)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
    else:
        command = sys.argv[1].lower()
        args = sys.argv[2:]
        if not isinstance(args, list):
            args = list(args)
        main(command=command, args=args)
