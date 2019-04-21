#!/usr/bin/env python3
"""ASMR video management"""
import os
import re
import sqlite3
import webbrowser
from collections import namedtuple
from pathlib import Path
from random import choice as random_choice

import click


Video = namedtuple('Video', 'title artist vid_id fav archived')
DB_FILENAME = str((Path(os.environ["DATADIR"]) / "data.database").resolve())


def format_video(video):
    """Prettyprint a Video"""
    fav = "F" if video.fav else "."
    arc = "@" if video.archived else "."
    return f"{fav} {arc} {video.artist:20s}{video.title}"


def display(entries):
    """For every asmr entry, display it's index and a pretty printed title"""
    title = f"   # F A {'ARTIST'.ljust(20)}TITLE"
    print(title)
    print("-"*(len(title)+20))
    for idx, (_, entry) in enumerate(entries):
        print(f"{idx:4} {format_video(entry)}")


def choose(entries, random=False):
    """Choose an entry from a entries, or get a random one."""
    if not entries:
        raise Exception("Can't choose. List is empty.")
    if random:
        return random_choice(entries)[1]
    if len(entries) == 1:
        return entries[0][1]
    display(entries)
    choice = int(input("Choose: "))
    return entries[choice][1]


@click.group()
def cli():
    """Handle asmr video data in $DATADIR/asmr.json.  Can view, add, play, or modify
    metadata.  Exists because youtube's playlists are pretty crap."""


@cli.command(short_help="Add a new video")
def add():
    """Give the user inputs to add a new video to the ASMRFILE"""
    artist = input("Artist: ")
    title = input("Title: ")
    vid = input("Video ID: ")
    fav = 1 if input("Fav [y/n]: ")[0] in ["Y", "y"] else 0

    if vid.startswith("www.") or vid.startswith("http"):
        match = re.search(".*?video=(.{11}).*", vid)
        if match:
            vid = match.group(1)
    if not vid:
        raise Exception("VidAddException: Could not parse video id")

    database = sqlite3.connect(DB_FILENAME)
    cursor = database.cursor()
    cursor.execute(f"""
        INSERT INTO asmr(title, artist, hash, fav, archived)
        VALUES ( '{title}', '{artist}', '{vid}', '{fav}', '{0}' )
    """)
    database.commit()
    database.close()


@cli.command(short_help="Modify a video")
@click.argument('query', nargs=-1)
def modify(query):
    """Modify an existing video's metadata"""
    query = ' '.join(query).lower()
    database = sqlite3.connect(DB_FILENAME)
    cursor = database.cursor()
    cursor.execute(f"""
        select * from asmr
        where title like '%{query}%' or artist like '%{query}%'
        ORDER BY artist, fav DESC, title
    """)
    data = cursor.fetchall()
    database.close()
    videos = [(idx, Video(title, artist, vid_id, fav, archived))
              for (idx, title, artist, vid_id, fav, archived) in data]
    display(videos)

    db_id, video = videos[int(input("Choose: "))]
    print(format_video(video))
    print("Enter new values, or leave blank to keep current")
    updates = []
    inp = input(f"artist ({video.artist}): ")
    if inp:
        updates.append(f"artist='{inp}'")
    inp = input(f"title ({video.title}): ")
    if inp:
        updates.append(f"title='{inp}'")
    inp = input(f"hash ({video.vid_id}): ")
    if inp:
        updates.append(f"hash='{inp}'")
    inp = input(f"fav ({video.fav}) (1/0): ")
    if inp:
        updates.append(f"fav={int(inp)}")
    inp = input(f"archived ({video.archived}) (1/0): ")
    if inp:
        updates.append(f"archived={int(inp)}")

    if not updates:
        return

    database = sqlite3.connect(DB_FILENAME)
    cursor = database.cursor()
    command = f"""
        UPDATE asmr
        SET {','.join(updates)}
        WHERE id={db_id}
    """
    cursor.execute(command)
    database.commit()


@cli.command(short_help="View list of videos")
@click.argument('query', nargs=-1)
@click.option('-f', '--only-favourites', is_flag=True, default=False)
@click.option('-a', '--with-archived', is_flag=True, default=False)
def view(query, only_favourites, with_archived):
    """List videos, optionally filtered by query or favourites only"""
    query = ' '.join(query).lower()
    fav = "AND fav = 1" if only_favourites else ""
    archived = "AND archived = 0" if not with_archived else ""
    database = sqlite3.connect(DB_FILENAME)
    cursor = database.cursor()
    cursor.execute(f"""
        select * from asmr
        where (title like '%{query}%' or artist like '%{query}%')
            {fav} {archived}
        ORDER BY artist, fav DESC, title""")
    data = cursor.fetchall()
    database.close()
    videos = [(idx, Video(title, artist, vid_id, fav, archived))
              for (idx, title, artist, vid_id, fav, archived) in data]
    display(videos)


@cli.command(short_help="Play a video")
@click.argument('query', nargs=-1)
@click.option('-r', '--random', is_flag=True, default=False)
@click.option('-f', '--only-favourites', is_flag=True, default=False)
@click.option('-a', '--with-archived', is_flag=True, default=False)
def play(query, random, only_favourites, with_archived):
    """Play a video (optionally filtered)"""
    query = ' '.join(query).lower()
    fav = "AND fav = 1" if only_favourites else ""
    archived = "AND archived = 0" if not with_archived else ""
    database = sqlite3.connect(DB_FILENAME)
    cursor = database.cursor()
    cursor.execute(f"""
        select * from asmr
        where (title like '%{query}%' or artist like '%{query}%')
            {fav} {archived} """)
    data = cursor.fetchall()
    database.close()
    videos = [(idx, Video(title, artist, vid_id, fav, archived))
              for (idx, title, artist, vid_id, fav, archived) in data]
    choice = choose(videos, random)
    print(format_video(choice))
    url = f"https://www.youtube.com/watch?v={choice.vid_id}"
    webbrowser.open(url)


cli()
