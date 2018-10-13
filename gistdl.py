#!/usr/bin/env python
import re
import os
from argparse import ArgumentParser
import requests


RX_LINK_MATCHER = re.compile(r"\[(.*?)\]\((.*?)\)")


def slugify(filename, keepcharacters=' ._-'):
    fn_out = ""
    for letter in filename.replace(' ', '-'):
        if letter.isalnum() or letter in keepcharacters:
            fn_out += letter
        else:
            fn_out += '-'    
    return re.sub("-+", "-", fn_out)


def get_markdown_links_from_gist(gist_url):
    response = requests.get(gist_url)
    link_groups = RX_LINK_MATCHER.findall(response.text)
    return {l[0]: l[1] for l in link_groups}


def check_files_needing_downloaded(download_dir, gist_url):
    entries = get_markdown_links_from_gist(gist_url)
    in_gist = {slugify(entry).lower() for entry in entries}
    filenames = {os.path.splitext(f)[0] for f in os.listdir(download_dir)}
    in_dir = {slugify(fname).lower() for fname in filenames}
    # Find files in the gist, but not yet downloaded
    needing_downloaded = in_gist - in_dir
    if needing_downloaded:
        print("Need to download:")
        for entry in needing_downloaded:
            print("\t", entry)
    # Find files in the directory, but not in the gist
    # (if you want to keep the contents mirrored)
    needing_added_to_gist = in_dir - in_gist
    if needing_added_to_gist:
        print("Need to update gist (potentially):")
        for entry in needing_added_to_gist:
            print("\t", entry)
    return 


if __name__ == '__main__':
    parser = ArgumentParser("gistdl", description="GIST markdown link downloader")
    parser.add_argument("GIST")
    parser.add_argument("DIRECTORY")
    parser.add_argument("--dl", help="Actually download missing files", action="store_true")
    args = parser.parse_args()
    check_files_needing_downloaded(args.DIRECTORY, args.GIST)
    if args.dl:
        print("IMPLEMENT DOWNLOAD")