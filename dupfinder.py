"""Find duplicates based on file hash.

Usage:
    dupFinder.py [--verbose] <folders>...

Options:
    -v --verbose   Show verbose output. [default: False]."""
# dupFinder.py
import os
import sys
import hashlib
from collections import defaultdict
from docopt import docopt

def find_duplicates(parent, verbose=False):
    """Find all duplicates within a parent folder."""
    dups = defaultdict(list) # {hash: filename}
    for directory, _, file_list in os.walk(parent):
        if verbose:
            print('Scanning {}...'.format(directory))
        for filename in file_list:
            path = os.path.join(directory, filename) # Get the path to the file
            if 'git' in path:
                if verbose:
                    print("Skipping {}".format(path))
                continue
            file_hash = hashfile(path) # Calculate hash
            dups[file_hash].append(path)
    return dups

def join_dicts(dict1, dict2):
    """Join two dictionaries."""
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]

def hashfile(path, blocksize=65536):
    """Get the hash digest of a file, using md5."""
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while buf:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def show_results(dict1):
    """Show the duplicates found."""
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if results:
        print('Duplicates Found.  These files have identical CONTENTS.')
        print('_' * 20)
        for result in results:
            for subresult in result:
                print('\t\t%s' % subresult)
            print('-' * 20)


def __main(folders, verbose):
    if not folders:
        print("Must provide at least 1 folder to check.")
    if not os.path.isdir(folders[0]):
        print("Must provide at least 1 folder to check.")
    dups = {}
    for folder in folders:
        if os.path.exists(folder):
            join_dicts(dups, find_duplicates(folder, verbose))
        else:
            print('{} is not a valid path, please verify'.format(folder))
            sys.exit()
    show_results(dups)


if __name__ == '__main__':
    ARGS = docopt(__doc__, version='0.0.1')
    __main(ARGS['<folders>'], ARGS['--verbose'])
