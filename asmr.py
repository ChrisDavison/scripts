#!/usr/bin/env python3
"""ASMR video management"""
import json
import os
import random
import re
import webbrowser
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Any

import click




@click.group()
def cli():
    """Handle asmr video data in $DATADIR/asmr.json.  Can view, add, play, or modify
    metadata.  Exists because youtube's playlists are pretty crap."""
    pass


@cli.command(short_help="Add a new video")
def add():
    """Give the user inputs to add a new video to the ASMRFILE"""
    videos.append((len(videos), Video.new()))
    write_asmr_file(videos)


@cli.command(short_help="View list of videos")
@click.argument('query', nargs=-1)
@click.option('-f', '--only-favourites', is_flag=True, default=False)
@click.option('-a', '--with-archived', is_flag=True, default=False)
def view(query, only_favourites, with_archived):
    """List videos, optionally filtered by query or favourites only"""
    filtered = filter_videos(' '.join(query), only_favourites, with_archived)
    display(filtered)


@cli.command(short_help="Modify a video")
@click.argument('query', nargs=-1)
def modify(query):
    """Modify an existing video's metadata"""
    query = ' '.join(query)
    options = [(i, video) for i, video in videos if query in video]
    for idx, (i, video) in enumerate(options):
        print(f"{idx:4} {video}")
    vid_choice = options[int(input("Choose: "))][0]
    print("\n", videos[vid_choice][1].__repr__(), "\n")
    options = ["artist", "title", "fav", "archived", "exit"]
    while True:
        response = input(", ".join(options) + ": ").lower()
        if response == "exit":
            break
        elif response not in options:
            break
        elif response == "artist":
            videos[vid_choice][1].artist = input("Artist: ")
        elif response == "title":
            videos[vid_choice][1].title = input("Title: ")
        elif response == "fav":
            videos[vid_choice][1].fav = not videos[vid_choice][1].fav
            print(f"'Favourite' toggled to {videos[vid_choice][1].fav}")
        elif response == "archived":
            videos[vid_choice][1].archived = not videos[vid_choice][1].archived
            print(f"'Archived' toggled to {videos[vid_choice][1].archived}")
        else:
            raise Exception("Shouldn't be possible to get here...'%s'" % response)
        print()
    print("\n", videos[vid_choice][1].__repr__())
    write_asmr_file(videos)


@cli.command(short_help="Play a video")
@click.argument('query', nargs=-1)
@click.option('-r', '--random', is_flag=True, default=False)
@click.option('-f', '--only-favourites', is_flag=True, default=False)
@click.option('-a', '--with-archived', is_flag=True, default=False)
def play(query, random, only_favourites, with_archived):
    """Play a video (optionally filtered)"""
    filtered = filter_videos(' '.join(query), only_favourites, with_archived)
    choice = choose(filtered, random) 
    print(choice)
    choice.open()


@dataclass
class Video:
    """An ASMR Video.

    Contains title, artist, ID (11-character), and indication of favourite
    """

    title: str
    artist: str
    vid_id: str
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
        url = f"https://www.youtube.com/watch?v={self.vid_id}"
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


def filter_videos(query, only_favourites, with_archived):
    filtered = []
    for i, vid in videos:
        has_query = query.lower() in vid
        has_fav = vid.fav or not only_favourites
        has_archive = not vid.archived or with_archived
        if has_query and has_fav and has_archive:
            filtered.append((i, vid))

        # if query.lower() in vid:
        #     has_query
    # filtered = [(i, vid) for (i, vid) in videos if query.lower() in vid]
    # if only_favourites:
        # filtered = [video for video in filtered if video.fav]
    # if not with_archived:
        # filtered = [video for video in filtered if not video.archived]
    return filtered


def display(entries: List[Video]):
    """For every asmr entry, display it's index and a pretty printed title"""
    title = f"   # F A {'ARTIST'.ljust(20)}TITLE"
    print(title)
    print("-"*(len(title)+20))
    for idx, (i, entry) in enumerate(entries):
        print(f"{idx:4} {entry}")
    

def load_asmr_file() -> List[Video]:
    """Read a json file and convert entries to Video."""
    videos = []
    for entry in json.load(open(FILENAME, encoding="utf8")):
        videos.append(Video(
            entry["title"],
            entry["artist"],
            entry["vid_id"],
            entry["fav"],
            entry["archived"]))
    return list(enumerate(sorted(videos, key=lambda x: x.artist)))


def write_asmr_file(videos):
    """Convert videos to a dict and then export to json file."""
    if not videos:
        raise Exception("Sent empty list of videos to write to file")
    json.dump([asdict(v) for i, v in videos], open(FILENAME, "w", encoding="utf8"), indent=2)


def choose(list, random=False):
    """Choose an entry from a list, or get a random one."""
    if random:
        return random.choice(list)[1]
    if not list:
        raise Exception("List is empty")
    if len(list) == 1:
        return list[0][1]
    display(list)
    choice = int(input("Choose: "))
    return list[choice][1]


try:
    direc = os.environ.get("DATADIR", None)
    if not direc:
        raise Exception("DATADIR not defined")
    FILENAME = str((Path(direc) / "asmr.json").resolve())
    videos = load_asmr_file()
    cli()
except Exception as E:
    print(E)
