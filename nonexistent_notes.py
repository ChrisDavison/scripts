#!/usr/bin/env python3 

import os 
import re 
from argparse import ArgumentParser


parser = ArgumentParser(description="Print broken local links in each file")
parser.add_argument("files", nargs="*")
parser.add_argument("--vimgrep", action='store_true')
args = parser.parse_args()


def get_links_in_file(filename):
    if not filename.endswith(".md"):
        return []
    re_file_link = re.compile(r"\((?:\./)*([a-zA-Z0-9\-_ ]*?\.md)")
    links =  []
    for i, line in enumerate(open(filename)):
        for m in re_file_link.finditer(line.lower()):
            links.append((i, m.span()[0], m.group(1)))
    return links

    
def print_broken_forwardlinks(filename, vimgrep_output):
    broken = [(i, j, link) for (i, j, link) in get_links_in_file(filename)
            if not os.path.exists(os.path.join(os.path.dirname(filename), link))]
    if broken:
        if vimgrep_output:
            for linum, colnum, link in broken:
                print("{}:{}:{}:{}".format(filename, linum+1, colnum+1, link))
        else:
            print(filename)
            for linum, colnum, link in broken:
                print("  >", link)


files = [f for f in os.listdir() if f.endswith(".md")]
if args.files:
    files = args.files
for filename in files:
    print_broken_forwardlinks(filename, args.vimgrep)

