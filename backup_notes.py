#!/usr/bin/env python3
"""Backup all notes (copy to another dir)"""
import os
import contextlib
from datetime import date
from pathlib import Path
from typing import List


@contextlib.contextmanager
def working_directory(path: Path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.

    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(prev_cwd)


def sync(root: Path, output: Path,
         exclude: List[str] = ['recipes'],
         msg: str = ""):
    """Sync all files from root to output."""
    input_files = {f.relative_to(root) for f in root.rglob('*.md')}
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
    files_to_copy = [str(root / filename)
                     for filename in input_being_added]
    with working_directory(output):
        today = date.today().strftime('%Y-%m-%d')
        if output_needing_deleted:
            for filename in output_needing_deleted:
                os.system(f"git rm {filename}")
        if input_being_added:
            os.system(f"rsync -v {' '.join(files_to_copy)} {output}")
            os.system('git add --all')
        if input_being_added or output_needing_deleted:
            os.system(f'git commit -m "backup {msg}: {today}"')


def main():
    # Root directories
    dir_dropbox = Path("~/Dropbox/").expanduser()
    dir_repo = Path("~/code/knowledge/").expanduser()
    # root directories
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
