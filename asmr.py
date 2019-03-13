#!/usr/bin/env python3
from enum import Enum
import argparse
import json
import os
import random
import re
import webbrowser


class Errors(Enum):
    """Enum for more descriptive error return values (sys.exit)"""
    none = 0
    no_vid = 1
    short_vid_hash = 2
    vid_already_exists = 3


class Style:
    """Shortcuts to terminal styling escape sequences"""
    BOLD = "\033[1m"
    END = "\033[0m"
    FG_Black = "\033[30m"
    FG_Red = "\033[31m"
    FG_Green = "\033[32m"
    FG_Yellow = "\033[33m"
    FG_Blue = "\033[34m"
    FG_Magenta = "\033[35m"
    FG_Cyan = "\033[36m"
    FG_White = "\033[37m"
    BG_Black = "\033[40m"
    BG_Red = "\033[41m"
    BG_Green = "\033[42m"
    BG_Yellow = "\033[43m"
    BG_Blue = "\033[44m"
    BG_Magenta = "\033[45m"
    BG_Cyan = "\033[46m"
    BG_White = "\033[47m"


def parse_youtube_video(url):
    """Take a youtube url and extract the video id hash"""
    match = re.search(".*?v=(.{11})", url)
    if match:
        return match.group(1)
    return None


def display(entries):
    """For every asmr entry, display it's index and a pretty printed title"""
    for i, entry in enumerate(entries):
        print(f"{i:4} {format_entry(entry)}")


def add_to(entries, filename):
    """Give the user prompts to add a new asmr video to the backend file"""
    artist = input("Artist: ")
    title = input("Title: ")
    fav = input("Fav [y/n]: ").lower()
    vid = input("Video ID: ")
    if vid.startswith('www.') or vid.startswith('http'):
        vid = parse_youtube_video(vid)
    if len(vid) < 11:
        raise Exception("VidAddException: Video hash must be >= 11 characters")
    if any(True for e in entries if e["hash"] == vid):
        raise Exception("VidAddException: Video already exists")
    new_vid = {
        "artist": artist,
        "title": title,
        "hash": vid,
        "fav": True if fav[0] == "y" else False,
        "broken": False
    }
    entries.append(new_vid)
    json.dump(entries, open(filename, "w", encoding="utf8"), indent=2)


def filter(query, entries):
    """Filter videos based on a matching title or artist"""
    q = query.lower()
    matches = [
        e for e in entries if q in e["title"].lower() or q in e["artist"].lower()
    ]
    if not matches:
        raise Exception("FilterException: No videos remain after filtering")
    return matches


def choose(entries, get_random_video=False):
    """Either prompt for a choice or return a random matching video"""
    choice = random.randint(0, len(entries) - 1)
    if not get_random_video:
        if len(entries) == 1:
            choice = 0
        else:
            display(entries)
            choice = int(input("Choice: "))
    return entries[choice]


def format_entry(video):
    """Pretty print an asmr video entry"""
    s = f"{Style.BOLD}{Style.FG_Red}" if video["fav"] else ""
    return f"{s}{video['artist']:20}{video['title']}{Style.END}"


def urlize(video):
    """Take an asmr video, and create a url from its hash"""
    return f"https://www.youtube.com/watch?v={video['hash']}"


def open_in_browser(video):
    """Use the default web browser to open ASMR video's url"""
    webbrowser.open(urlize(video))


def main():
    """Run asmr video listing or choice"""
    try:
        parser = argparse.ArgumentParser("asmr")
        flags = parser.add_mutually_exclusive_group()
        flags.add_argument("-r", help="Open a random video", action="store_true")
        flags.add_argument("-a", help="Add a video", action="store_true")
        flags.add_argument("-l", help="List videos", action="store_true")
        flags.add_argument("-f", help="List favourite videos", action="store_true")
        flags.add_argument("-b", help="List broken videos", action="store_true")
        parser.add_argument("query", help="Query to filter by", nargs="*", default="")
        args = parser.parse_args()

        filename = os.path.expanduser("~/Dropbox/data/asmr.json")
        vids = json.load(open(filename, encoding="utf8"))
        vids = sorted(vids, key=lambda x: x["artist"])
        vids = filter(' '.join(args.query), vids)

        if args.a:
            add_to(vids, filename)
        elif args.l:
            display(vids)
        elif args.f:
            display([v for v in vids if v['fav']])
        elif args.b:
            display([v for v in vids if v['broken']])
        else:
            choice = choose(vids, args.r)
            print(format_entry(choice))
            print(urlize(choice))
            open_in_browser(choice)
    except (EOFError, KeyboardInterrupt):
        print("\nNo video selected. Exiting...")
    except Exception as E:
        print(E)


if __name__ == "__main__":
    main()

