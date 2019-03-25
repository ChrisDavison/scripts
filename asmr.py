#!/usr/bin/env python3
"""ASMR video management.

Optionally filtered by QUERY (matching title or artist).

usage:
    asmr add
    asmr view [-f] [QUERY...]
    asmr open [-r|-f] [QUERY...]

options:
    -a          Add a new video
    -r          Open a random video [default: False]
    -f          Filter to favourites only [default: False]
"""
from enum import Enum
import argparse
import json
import os
import random
import re
import webbrowser
from dataclasses import dataclass, asdict
from typing import List, Optional, Any

from docopt import docopt

from terminalstyle import Style


class Errors(Enum):
    """Enum for more descriptive error return values (sys.exit)"""

    none = 0
    no_vid = 1
    short_vid_hash = 2
    vid_already_exists = 3


@dataclass
class Video:
    """An ASMR Video.

    Contains title, artist, ID (11-character), and indication of favourite
    """

    title: str
    artist: str
    hash: str
    fav: bool

    def __contains__(self, query):
        q = query.lower()
        return q in self.title.lower() or q in self.artist.lower()

    def __str__(self):
        s = f"{Style.BOLD}{Style.FG_Red}" if self.fav else ""
        return f"{s}{self.artist:20}{self.title}{Style.END}"

    def open(self):
        url = f"https://www.youtube.com/watch?v={self.hash}"
        webbrowser.open(url)


def write_vids(videos, filename):
    entries = [asdict(v) for v in videos]
    json.dump(entries, open(filename, "w", encoding="utf8"), indent=2)


def display(entries):
    """For every asmr entry, display it's index and a pretty printed title"""
    for i, entry in enumerate(entries):
        print(f"{i:4} {entry}")


def new_video():
    """Give the user prompts to create a new asmr video."""
    artist = input("Artist: ")
    title = input("Title: ")
    fav = input("Fav [y/n]: ").lower()
    vid = input("Video ID: ")

    def parse_youtube_video(url):
        """Take a youtube url and extract the video hash hash"""
        match = re.search(".*?v=(.{11})", url)
        if match:
            return match.group(1)
        return None

    if vid.startswith("www.") or vid.startswith("http"):
        vid = parse_youtube_video(vid)
    if len(vid) < 11:
        raise Exception("VidAddException: Video hash must be >= 11 characters")
    return Video(title, artist, hash, fav) 
    

def load_from_json() -> List[Video]:
    filename = os.path.expanduser("~/Dropbox/data/asmr.json")
    vids = json.load(open(filename, encoding="utf8"))

    def json_to_Video(j):
        return Video(j["title"], j["artist"], j["hash"], j["fav"])

    return [json_to_Video(j) for j in vids]


def main():
    """Run asmr video listing or choice"""
    try:
        args = docopt(__doc__)

        vids = load_from_json()
        q = " ".join(args["QUERY"])
        filtered = [v for v in vids if q in v]
        if args['-f']:
            filtered = [v for v in filtered if v.fav]

        if args["add"]:
            old_vids = vids
            vids.append(new_video())
            if set(vids) == set(old_vids):
                print("No change!")
            else:
                pass
            # print("Not re-implemented yet")
            # add_to(vids, filename)
        elif args["view"]:
            display(filtered)
        else:
            choiceidx = random.randint(0, len(filtered) - 1)
            if not args['-r']:
                if len(filtered) == 1:
                    choice = 0
                else:
                    display(filtered)
                choiceidx = int(input("Choice: "))
            choice = filtered[choiceidx]
            print(choice)
            choice.open()
    except (EOFError, KeyboardInterrupt):
        print("\nNo video selected. Exiting...")
    except Exception as E:
        print(E)


if __name__ == "__main__":
    main()
