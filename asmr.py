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
import click


direc = os.environ.get("DATADIR", None)
if not direc:
    raise Exception("DATADIR not defined")
FILENAME = str((Path(direc) / "asmr.json").resolve())


@click.group()
def cli():
    """ASMR video management.

    Optionally filtered by QUERY (matching title or artist).
    Looks for 'asmr.json' inside directory defined by $DATADIR, with title, artist, 
    hash, and fav keys.

    This script exists because youtube's playlists are pretty balls, and I wanted an
    easier way of jumping to videos based on keyword matches (e.g. if I want to
    watch a tapping video)."""
    pass


@cli.command(short_help="Add a new video")
def add():
    pass


@cli.command(short_help="View list of videos")
@click.argument('query', nargs=-1)
@click.option('-f', '--with-favourites', is_flag=True, default=False)
@click.option('-a', '--with-archived', is_flag=True, default=False)
def view(query, with_favourites, with_archived):
    filtered = load_from_json()
    if with_favourites:
        filtered = [video for video in filtered if video.fav]
    if not with_archived:
        filtered = [video for video in filtered if not video.archived]
    display(filtered)


@cli.command(short_help="Modify a video")
@click.argument('query', nargs=-1)
def modify(query):
    pass


@cli.command(short_help="Play a video")
@click.argument('query', nargs=-1)
@click.option('-r', '--random', is_flag=True, default=False)
def play(query, random):
    print(' '.join(query), random)




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
            match = re.search(".*?video=(.{11}).*", url)
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


# def write_vids(videos: List[Video]):
#     if not videos:
#         raise Exception("Sent empty list of videos to write to file")
#     def replace_vid_to_hash(video):
#         h = video["vid"]
#         del video["vid"]
#         return {"hash": h, **video}

#     entries = [replace_vid_to_hash(asdict(video)) for video in videos]
#     if not entries:
#         raise Exception("Entries in write_vids is empty")
#     json.dump(entries, open(FILENAME, "w", encoding="utf8"), indent=2)


# def modify(vids, query):
#     for i, video in enumerate(vids):
#         if query in video:
#             print(i, video)
#     vid_choice = int(input("Choose: "))
#     print(vids[vid_choice].__repr__())
#     print()
#     options = ["artist", "title", "fav", "archived", "exit"]
#     while True:
#         response = input(", ".join(options) + ": ").lower()
#         if response == "exit":
#             break
#         elif response not in options:
#             break
#         elif response == "artist":
#             vids[vid_choice].artist = input("Artist: ")
#         elif response == "title":
#             vids[vid_choice].title = input("Title: ")
#         elif response == "fav":
#             vids[vid_choice].fav = not vids[vid_choice].fav
#             print(f"'Favourite' toggled to {vids[vid_choice].fav}")
#         elif response == "archived":
#             vids[vid_choice].archived = not vids[vid_choice].archived
#             print(f"'Archived' toggled to {vids[vid_choice].archived}")
#         else:
#             raise Exception("Shouldn't be possible to get here...'%s'" % response)
#     print(vids[vid_choice].__repr__())
#     print()
#     happy = input("Happy? [y/n] ").lower()[0] == "y"
#     if not happy:
#         raise Exception("Not happy with result. Re-run if needed")
#     write_vids(vids)


# def choose(list, random=False):
#     if random:
#         return list[random.randint(0, len(list) - 1)]
#     if not list:
#         raise Exception("List is empty")
#     if len(list) == 1:
#         return list[0]
#     display(list)
#     choice = int(input("Choose: "))
#     return list[choice]
        

# def main():
#     """Run asmr video listing or choice"""
#     args = docopt(__doc__)
#     vids = load_from_json()
#     query = " ".join(args["QUERY"])
#     filtered = [video for video in vids if query in video]
#     if args["-f"]:
#         filtered = [video for video in filtered if video.fav]
#     if not args["-a"]:
#         filtered = [video for video in filtered if not video.archived]


#     try:
#         if args["add"]:
#             old_vids = vids.copy()
#             vids.append(Video.new())
#             write_vids(vids)
#         elif args["view"]:
#             display(filtered)
#         elif args["modify"]:
#             modify(vids, query)
#         elif args["open"]:
#             choice = choose(filtered, args["-r"]) 
#             print(choice)
#             choice.open()
#         else:
#             print("Unknown option...shouldn't be able to get here")

# try:
cli()
# except Exception as E:
    # print(E)
