#!/usr/bin/env python3
"""List all files for a dropbox account (token)"""
import os
import dropbox


def get_folders(token, path, ignore):
    """List all folders, recursively"""
    response = dropbox.Dropbox(token).files_list_folder(path)
    out = [path]
    is_folder = lambda x: isinstance(x, dropbox.files.FolderMetadata)
    for folder in filter(is_folder, response.entries):
        path = folder.path_lower
        if len(path.split("/")) < 5 and not any(i.lower() in path for i in ignore):
            out.extend(get_folders(token, folder.path_lower, ignore))
    return out


def indented_str(path, max_level):
    parts = path.split("/")
    indent = len(parts) - 2
    if indent == 0:
        out = "\n# " + parts[-1] + "\n\n"
    elif indent <= max_level:
        out = "- `|{} {}`".format("-" * indent * 2, parts[-1])
    else:
        out = ""
    return out


if __name__ == "__main__":
    TOKEN = open(os.path.expanduser('~/.dropbox-token')).read().split('\n')[0]
    NON_EMPTY_PATHS = filter(lambda x: x != "", get_folders(TOKEN, "", ["Camera Uploads"]))
    with open("contents-tree.md", "w") as f_out:
        for path in sorted(NON_EMPTY_PATHS):
            print(indented_str(path, max_level=10), file=f_out)
