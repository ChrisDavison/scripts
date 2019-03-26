#!/usr/bin/env python3
"""ASMR video management.

Optionally filtered by QUERY (matching title or artist).
Looks for 'asmr.json' inside directory defined by $DATADIR, with title, artist, 
hash, and fav keys.

This script exists because youtube's playlists are pretty balls, and I wanted an
easier way of jumping to videos based on keyword matches (e.g. if I want to
watch a tapping video).

usage:
    asmr add
    asmr view [-f] [QUERY...]
    asmr open [-r|-f] [QUERY...]

options:
    -f          Filter to favourites only [default: False]
    -r          Open a random video [default: False]
"""
import json
import os
import random
import re
import webbrowser
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Any

from docopt import docopt


@dataclass
class Video:
    """An ASMR Video.

    Contains title, artist, ID (11-character), and indication of favourite
    """

    title: str
    artist: str
    vid: str
    fav: bool

    def __contains__(self, query):
        q = query.lower()
        return q in self.title.lower() or q in self.artist.lower()

    def __str__(self):
        BOLD = "\033[1m"
        END = "\033[0m"
        FG_Red = "\033[31m"
        s = f"{BOLD}{FG_Red}" if self.fav else ""
        return f"{s}{self.artist:20}{self.title}{END}"

    def open(self):
        url = f"https://www.youtube.com/watch?v={self.vid}"
        webbrowser.open(url)


def get_filename():
    direc = os.environ.get('DATADIR', None)
    if not direc:
        raise Exception("DATADIR not defined")
    return str((Path(direc) / 'asmr.json').resolve())


def display(entries: List[Video]):
    """For every asmr entry, display it's index and a pretty printed title"""
    for i, entry in enumerate(entries):
        print(f"{i:4} {entry}")


def new_video() -> Video:
    """Give the user prompts to create a new asmr video."""
    artist = input("Artist: ")
    title = input("Title: ")
    vid = input("Video ID: ")
    fav = input("Fav [y/n]: ")[0] in ['Y', 'y']

    def parse_youtube_video(url):
        """Take a youtube url and extract the video hash"""
        match = re.search(".*?v=(.{11})", url)
        if match:
            return match.group(1)
        return None

    if vid.startswith("www.") or vid.startswith("http"):
        vid = parse_youtube_video(vid)
    if len(vid) < 11:
        raise Exception("VidAddException: Video hash must be >= 11 characters")
    return Video(title, artist, vid, fav) 
    

def load_from_json() -> List[Video]:
    vids = json.load(open(get_filename(), encoding="utf8"))

    def json_to_Video(j):
        return Video(j["title"], j["artist"], j["hash"], j["fav"])

    return [json_to_Video(j) for j in vids]


def write_vids(videos: List[Video]):
    def replace_vid_to_hash(v):
        h = v['vid']
        del v['vid']
        return {'hash': h, **v}

    entries = [replace_vid_to_hash(asdict(v)) for v in videos]
    json.dump(entries, open(get_filename(), "w", encoding="utf8"), indent=2)


def main():
    """Run asmr video listing or choice"""
    args = docopt(__doc__)
    vids = load_from_json()
    q = " ".join(args["QUERY"])
    filtered = [v for v in vids if q in v]
    if args['-f']:
        filtered = [v for v in filtered if v.fav]

    try:
        if args["add"]:
            old_vids = vids.copy()
            vids.append(new_video())
            if not list(set(v.vid for v in vids)) == list(set(v.vid for v in
                old_vids)):
                write_vids(vids)
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
