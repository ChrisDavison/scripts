"""Find duplicates based on file hash.

Usage:
    dupFinder.py [--verbose] <folders>...

Options:
    -v --verbose   Show verbose output. [default: False]."""
# dupFinder.py
import os, sys
import hashlib
from docopt import docopt
from collections import defaultdict

def findDup(parentFolder, verbose=False):
    dups = defaultdict(list) # {hash: filename}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        if verbose:
            print('Scanning {}...'.format(dirName))
        for filename in fileList:
            path = os.path.join(dirName, filename) # Get the path to the file
            if 'git' in path:
                if verbose:
                    print("Skipping {}".format(path))
                continue
            file_hash = hashfile(path) # Calculate hash
            dups[file_hash].append(path)
    return dups

def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]

def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if results:
        print('Duplicates Found.  These files have identical CONTENTS.')
        print('_' * 20)
        for result in results:
            for subresult in result:
                print('\t\t%s' % subresult)
            print('-' * 20)

if __name__ == '__main__':
    args = docopt(__doc__, version='0.0.1')
    folders = args['<folders>']
    verbose = args['--verbose']
    if not folders:
        print("Must provide at least 1 folder to check.")
    if not os.path.isdir(folders[0]):
        print("Must provide at least 1 folder to check.")
    dups = {}
    for folder in folders:
        if os.path.exists(folder):
            joinDicts(dups, findDup(folder, verbose))
        else:
            print('{} is not a valid path, please verify'.format(folder))
            sys.exit()
    printResults(dups)
