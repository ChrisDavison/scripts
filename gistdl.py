#!/usr/bin/env python
import re
from pathlib import Path
from argparse import ArgumentParser
import requests
import youtubedl


RX_LINK_MATCHER = re.compile(r"\[(.*?)\]\((.*?)\)")


def slugify(filename, keepcharacters="._-"):
    """Remove unsuitable characters and return a better filename."""

    def get_good_character(letter):
        """Close over the parent's keepcharacters to replace unsuitable letters in filename"""
        if letter.isalnum() or letter in keepcharacters:
            return letter
        return "-"

    fn_out = "".join([get_good_character(letter) for letter in filename])
    return re.sub("-+", "-", fn_out)


def markdown_links_from_gist(gist_url):
    """Get a dict of {title:url} from a raw Github GIST containing markdown links."""
    response = requests.get(gist_url).text
    return {l[0]: l[1] for l in RX_LINK_MATCHER.findall(response)}


def files_missing_from_gist(links, directory):
    """Get files that exist locally but aren't in the gist."""
    links_as_filenames = {slugify(title).lower(): title for title in links}
    filenames = {slugify(Path(f).stem).lower() for f in directory.glob("*")}
    return filenames - set(links_as_filenames.keys())


def files_not_yet_downloaded(links, directory):
    """Get files that are in the gist, but not downloaded."""
    links_as_filenames = {slugify(title).lower(): title for title in links}
    filenames = {slugify(Path(f).stem).lower() for f in directory.glob("*")}
    return set(links_as_filenames.keys()) - filenames


def _main():
    """Download all youtube videos in a GIST, looking for markdown-syntax links."""
    parser = ArgumentParser("gistdl", description="GIST markdown link downloader")
    parser.add_argument("GIST")
    parser.add_argument("DIRECTORY")
    parser.add_argument("--dl", help="Download missing files", action="store_true")
    parser.add_argument("--print", help="Show missing files", action="store_true")
    args = parser.parse_args()
    direc = Path(args.DIRECTORY)
    links = markdown_links_from_gist(args.GIST)
    needing_bookmarked = files_missing_from_gist(links, direc)
    needing_downloaded = files_not_yet_downloaded(links, direc)
    if args.print:
        print("Need to bookmark (potentially):")
        for entry in sorted(needing_bookmarked):
            print("\t", entry)
        print("Need to download:")
        for entry in sorted(needing_downloaded):
            print("\t", entry)
    if args.dl:
        for title, url in needing_downloaded.items():
            fn_out = direc / slugify(title)
            youtubedl.download_video(url, filename=fn_out)


if __name__ == "__main__":
    _main()
