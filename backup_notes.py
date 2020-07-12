#!/usr/bin/env python3
"""Backup all notes (copy to another dir)"""
import os
import contextlib
from datetime import date
from pathlib import Path


@contextlib.contextmanager
def working_directory(path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.

    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(prev_cwd)


def sync(input, output, exclude=['recipes'], msg=""):
    input_files = {f.relative_to(input) for f in input.rglob('*.md')}
    filename_has_exclude = lambda f: set(f.parts) == (set(f.parts) - set(exclude))
    exclude = set(exclude)
    output_files = set()
    for filename in output.rglob('*.md'):
        parts = set(filename.parts)
        if len(parts) == len(parts - exclude):
            output_files.add(filename.relative_to(output))
    output_needing_deleted = output_files - input_files
    input_being_added = input_files - output_files
    print(f"{len(input_files)} files total", end='')
    print(f" - {len(output_needing_deleted)} being removed,", end='')
    print(f" {len(input_being_added)} being added")
    files_to_copy = ' '.join(str(input / filename)
            for filename in input_being_added)
    files_to_remove = ' '.join(str(output / filename)
            for filename in output_needing_deleted)
    with working_directory(output):
        today = date.today().strftime('%Y-%m-%d')
        if output_needing_deleted:
            for filename in output_needing_deleted:
                    os.system(f"git rm {filename}")
        if input_being_added:
            os.system(f'rsync -v {files_to_copy} {output}')
            os.system(f'git add --all')
        if input_being_added or output_needing_deleted:
            os.system(f'git commit -m "backup {msg}: {today}"')


def main():
    # Root directories
    dir_dropbox = Path("~/Dropbox/").expanduser()
    dir_repo = Path("~/code/knowledge/").expanduser()
    dir_zips = dir_dropbox / "archive"
    # Input directories
    dir_notes = dir_dropbox / "notes"
    dir_recipes = dir_dropbox / "recipes"
    # Output directories
    dir_notes_out = dir_repo
    dir_recipes_out = dir_repo / "recipes"
    print("Backing up notes")
    sync(dir_notes, dir_notes_out, msg='notes')
    print("\nBacking up recipes")
    sync(dir_recipes, dir_recipes_out, msg='recipes', exclude=[])


if __name__ == "__main__":
    main()
