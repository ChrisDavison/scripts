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
    asmr view [-f] [-a] [QUERY...]
    asmr open [-r|-f] [QUERY...]

options:
    -f          Filter to favourites only [default: False]
    -r          Open a random video [default: False]
    -a          Show all, including archived videos [default: False]
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
    archived: bool

    def __contains__(self, query):
        q = query.lower()
        return q in self.title.lower() or q in self.artist.lower()

    def __str__(self):
        BOLD = "\033[1m"
        END = "\033[0m"
        FG_Red = "\033[31m"
        s = f"{BOLD}{FG_Red}" if self.fav else ""
        arc = " (a)" if self.archived else ""
        return f"{s}{self.artist:20}{self.title}{arc}{END}"

    def open(self):
        url = f"https://www.youtube.com/watch?v={self.vid}"
        webbrowser.open(url)


def get_filename():
    direc = os.environ.get("DATADIR", None)
    if not direc:
        raise Exception("DATADIR not defined")
    return str((Path(direc) / "asmr.json").resolve())


def display(entries: List[Video]):
    """For every asmr entry, display it's index and a pretty printed title"""
    for i, entry in enumerate(entries):
        print(f"{i:4} {entry}")


def new_video() -> Video:
    """Give the user prompts to create a new asmr video.
    
    Always assumes a new video is not archived."""
    artist = input("Artist: ")
    title = input("Title: ")
    vid = input("Video ID: ")
    fav = input("Fav [y/n]: ")[0] in ["Y", "y"]

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
    return Video(title, artist, vid, fav, False)


def load_from_json() -> List[Video]:
    vids = json.load(open(get_filename(), encoding="utf8"))

    def json_to_Video(j):
        return Video(j["title"], j["artist"], j["hash"], j["fav"], j["archived"])

    return sorted([json_to_Video(j) for j in vids], key=lambda x: x.artist)


def write_vids(videos: List[Video]):
    def replace_vid_to_hash(v):
        h = v["vid"]
        del v["vid"]
        return {"hash": h, **v}

    entries = [replace_vid_to_hash(asdict(v)) for v in videos]
    json.dump(entries, open(get_filename(), "w", encoding="utf8"), indent=2)


def main():
    """Run asmr video listing or choice"""
    args = docopt(__doc__)
    vids = load_from_json()
    q = " ".join(args["QUERY"])
    filtered = [v for v in vids if q in v]
    if args["-f"]:
        filtered = [v for v in filtered if v.fav]
    if not args["-a"]:
        filtered = [v for v in filtered if not v.archived]

    try:
        if args["add"]:
            old_vids = vids.copy()
            vids.append(new_video())
            if not list(set(v.vid for v in vids)) == list(set(v.vid for v in old_vids)):
                write_vids(vids)
        elif args["view"]:
            display(filtered)
        elif args["open"] and args["-r"]:
            choiceidx = random.randint(0, len(filtered) - 1)
            choice = filtered[choiceidx]
            print(choice)
            choice.open()
        else:
            if len(filtered) == 1:
                print(f"Only 1 video: {filtered[0]}")
                play = input("Play? [y/n] ")[0].lower()
                if play == "y":
                    filtered[0].open()
            else:
                display(filtered)
                choice = int(input("Choose: "))
                print(filtered[choice])
                filtered[choice].open()
    except (EOFError, KeyboardInterrupt):
        print("\nNo video selected. Exiting...")
    except Exception as E:
        print(E)


if __name__ == "__main__":
    main()
