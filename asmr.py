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
    asmr modify QUERY...

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


direc = os.environ.get("DATADIR", None)
if not direc:
    raise Exception("DATADIR not defined")
FILENAME = str((Path(direc) / "asmr.json").resolve())


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
        query = query.lower()
        return query in self.title.lower() or query in self.artist.lower()

    def __str__(self):
        fav = "F" if self.fav else " "
        arc = "@" if self.archived else " "
        return f"{fav} {arc} {self.artist:20s}{self.title}"

    def __repr__(self):
        fav = "F" if self.fav else "x"
        arc = "@" if self.archived else "x"
        return f"[{fav}|{arc}] {self.title} by {self.artist}"

    def open(self):
        url = f"https://www.youtube.com/watch?v={self.vid}"
        webbrowser.open(url)

    @staticmethod
    def new():
        """Give the user prompts to create a new asmr video.
        
        Always assumes a new video is not archived."""
        artist = input("Artist: ")
        title = input("Title: ")
        vid = input("Video ID: ")
        fav = input("Fav [y/n]: ")[0] in ["Y", "y"]

        def parse_youtube_video(url):
            """Take a youtube url and extract the video hash"""
            match = re.search(".*?video=(.{11})", url)
            if match:
                return match.group(1)
            return None

        if vid.startswith("www.") or vid.startswith("http"):
            vid = parse_youtube_video(vid)
        if len(vid) < 11:
            raise Exception("VidAddException: Video hash must be >= 11 characters")
        return Video(title, artist, vid, fav, False)


def display(entries: List[Video]):
    """For every asmr entry, display it's index and a pretty printed title"""
    title = f"   # F A {'ARTIST'.ljust(20)}TITLE"
    print(title)
    print("-"*(len(title)+20))
    for i, entry in enumerate(entries):
        print(f"{i:4} {entry}")
    

def load_from_json() -> List[Video]:
    vids = json.load(open(FILENAME, encoding="utf8"))

    def json_to_Video(j):
        return Video(j["title"], j["artist"], j["hash"], j["fav"], j["archived"])

    return sorted([json_to_Video(j) for j in vids], key=lambda x: x.artist)


def write_vids(videos: List[Video]):
    def replace_vid_to_hash(video):
        h = video["vid"]
        del video["vid"]
        return {"hash": h, **video}

    entries = [replace_vid_to_hash(asdict(video)) for video in videos]
    json.dump(entries, open(FILENAME, "w", encoding="utf8"), indent=2)


def modify(vids, query):
    for i, video in enumerate(vids):
        if query in video:
            print(i, video)
    vid_choice = int(input("Choose: "))
    vid = vids[vid_choice]
    print(vid.__repr__())
    while True:
        print("Fields")
        print("\t0 Artist")
        print("\t1 Title")
        print("\t2 Fav")
        print("\t3 Archived")
        field_choice = int(input("> "))
        if field_choice < 0 or field_choice > 3:
            break
        if field_choice == 0:
            vids[vid_choice].artist = input("Artist: ")
        elif field_choice == 1:
            vids[vid_choice].title = input("Title: ")
        elif field_choice == 2:
            vids[vid_choice].fav = not vids[vid_choice].fav
            print(f"'Favourite' toggled to {vids[vid_choice].fav}")
        else:
            vids[vid_choice].archived = not vids[vid_choice].archived
            print(f"'Archived' toggled to {vids[vid_choice].archived}")
    vid = vids[vid_choice]
    print(vid.__repr__())
    happy = input("Happy? [y/n] ").lower()[0]
    if happy == "y":
        write_vids(vids)
    else:
        print("Not saving updates.  Re-run if needed")
        

def main():
    """Run asmr video listing or choice"""
    args = docopt(__doc__)
    vids = load_from_json()
    query = " ".join(args["QUERY"])
    filtered = [video for video in vids if query in video]
    if args["-f"]:
        filtered = [video for video in filtered if video.fav]
    if not args["-a"]:
        filtered = [video for video in filtered if not video.archived]


    try:
        if args["add"]:
            old_vids = vids.copy()
            vids.append(Video.new())
            write_vids(vids)
        elif args["view"]:
            display(filtered)
        elif args["modify"]:
            modify(vids, query)
        elif args["open"] and args["-r"]:
            choiceidx = random.randint(0, len(filtered) - 1)
            choice = filtered[choiceidx]
            print(choice)
            choice.open()
        else:
            choice = 0
            if len(filtered) > 1:
                display(filtered)
                choice = int(input("Choose: "))
            print(filtered[choice])
            print(filtered[choice].vid)
            filtered[choice].open()
    except (EOFError, KeyboardInterrupt):
        print("\nC-c pressed. Exiting...")
    except Exception as E:
        print(E)


if __name__ == "__main__":
    main()
