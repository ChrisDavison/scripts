#!/usr/bin/env python
import re
import os
from argparse import ArgumentParser
import requests
import youtubedl


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


def get_directory_contents(directory):
    filenames = {os.path.splitext(f)[0] for f in os.listdir(directory)}
    return {slugify(fname).lower() for fname in filenames}


def compare_links_and_directory(links, directory):
    links_as_filenames = {slugify(title).lower(): title for title in links}
    filenames = get_directory_contents(directory)
    needing_downloaded = set(links_as_filenames.keys()) - filenames
    if needing_downloaded:
        print("Need to download:")
        for entry in needing_downloaded:
            print("\t", entry)
    # Find files in the directory, but not in the gist
    # (if you want to keep the contents mirrored)
    needing_added_to_gist = filenames - set(links_as_filenames.keys())
    if needing_added_to_gist:
        print("Need to update gist (potentially):")
        for entry in needing_added_to_gist:
            print("\t", entry)
    return {title:url for title, url in links.items() if
            slugify(title).lower() in needing_downloaded}



if __name__ == '__main__':
    parser = ArgumentParser("gistdl", description="GIST markdown link downloader")
    parser.add_argument("GIST")
    parser.add_argument("DIRECTORY")
    parser.add_argument("--dl", help="Actually download missing files", action="store_true")
    args = parser.parse_args()
    links = get_markdown_links_from_gist(args.GIST)
    needing_downloaded = compare_links_and_directory(links, args.DIRECTORY)
    if args.dl:
        for title, url in needing_downloaded.items():
            fn_out = os.path.join(args.DIRECTORY, slugify(title))
            youtubedl.download(url, filename=fn_out)