#!/usr/bin/env python3
from enum import Enum
import argparse
import json
import os
import random
import re
import sys
import webbrowser


class Errors(Enum):
    none = 0
    no_vid = 1
    short_vid_hash = 2
    vid_already_exists = 3


class style:
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


def parse_youtube_video(s):
    m = re.search(".*?v=(.{11})", s)
    if m:
        return m.group(1)
    return None


def display(entries):
    for i, entry in enumerate(entries):
        print(f"{i:4} {format_entry(entry)}")


def add_to(entries, filename):
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
        "fav": True if fav[0] == "y" else False,
        "hash": vid,
    }
    entries.append(new_vid)
    json.dump(entries, open(filename, "w", encoding="utf8"), indent=2)


def filter(query, entries):
    q = query.lower()
    matches = [
        e for e in entries if q in e["title"].lower() or q in e["artist"].lower()
    ]
    if not matches:
        raise Exception("FilterException: No videos remain after filtering")
    return matches


def choose(entries, get_random_video=False):
    choice = random.randint(0, len(entries) - 1)
    if not get_random_video:
        if len(entries) == 1:
            choice = 0
        else:
            display(entries)
            choice = int(input("Choice: "))
    return entries[choice]


def format_entry(e):
    s = f"{style.BOLD}{style.FG_Red}" if e["fav"] else ""
    return f"{s}{e['artist']:20}{e['title']}{style.END}"


def urlize(e):
    return f"https://www.youtube.com/watch?v={e['hash']}"

def open_in_browser(e):
    webbrowser.open(urlize(e))


try:
    parser = argparse.ArgumentParser("asmr")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", help="Open a random video", action="store_true")
    group.add_argument("-a", help="Add a video", action="store_true")
    group.add_argument("-l", help="List videos", action="store_true")
    group.add_argument("-f", help="List favourite videos", action="store_true")
    parser.add_argument("query", help="Query to filter by", nargs="?", default="")
    args = parser.parse_args()

    filename = os.path.expanduser("~/Dropbox/data/asmr.json")
    vids = json.load(open(filename, encoding="utf8"))
    vids = sorted(vids, key=lambda x: x["artist"])
    vids = filter(args.query, vids)

    if args.a:
        add_to(vids, filename)
    elif args.l:
        display(vids)
    elif args.f:
        display([v for v in vids if v['fav']])
    else:
        choice = choose(vids, args.r == True)
        print(format_entry(choice))
        print(urlize(choice))
        open_in_browser(choice)
except (EOFError, KeyboardInterrupt):
    print("\nNo video selected. Exiting...")
except Exception as E:
    print(E)