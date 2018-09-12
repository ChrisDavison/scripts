import sys
import dropbox


__TOKEN = ''
dbx = dropbox.Dropbox(__TOKEN)


def get_folders_under_path(path, ignores):
    response = dbx.files_list_folder(path)
    out = [path]
    isFolder = lambda x: isinstance(x, dropbox.files.FolderMetadata)
    for f in filter(isFolder, response.entries):
        p = f.path_lower
        if len(p.split('/')) < 5 and not any (i.lower() in p for i in ignores):
            out.extend(get_folders_under_path(f.path_lower, ignores))
    return out


def indented_str(path, max_level):
    parts = path.split('/')
    indent = len(parts) - 2
    if indent == 0:
        out = '\n# ' + parts[-1] + '\n\n'
    elif indent <= max_level:
        out = "- `|{} {}`".format('-' * indent * 2, parts[-1])
    else:
        out = ""
    return out


if __name__ == '__main__':
    paths = [p 
             for p in get_folders_under_path("", ['Apps', 'Camera Uploads'])
             if p is not '']
    with open('contents-tree.md', 'w') as f_out:
        for p in sorted(paths):
            print(indented_str(p, max_level=10), file=f_out)