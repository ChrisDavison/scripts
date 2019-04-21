#!/usr/bin/env python3
"""ASMR video management"""
import os
import re
import sqlite3
import webbrowser
from random import choice as random_choice
from dataclasses import dataclass
from pathlib import Path

import click


DB_FILENAME = 'e:/Dropbox/data/data.db'


def execute_select(query):
    """Execute an sqlite select query, returning column names and data"""
    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = list(map(lambda x: x[0], cursor.description))
    db.close()
    return columns, data


@click.group()
def cli():
    """Handle asmr video data in $DATADIR/asmr.json.  Can view, add, play, or modify
    metadata.  Exists because youtube's playlists are pretty crap."""
    pass


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

    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    cursor.execute(f"""
        INSERT INTO asmr(title, artist, hash, fav, archived)
        VALUES ( '{title}', '{artist}', '{vid}', '{fav}', '{0}' )
    """)
    db.commit()
    db.close()


@cli.command(short_help="Modify a video")
@click.argument('query', nargs=-1)
def modify(query):
    """Modify an existing video's metadata"""
    query = ' '.join(query).lower()
    sql_query = f"""
        select * from asmr
        where title like '%{query}%' or artist like '%{query}%'
        ORDER BY artist, fav DESC, title
    """
    _, data = execute_select(sql_query)
    videos = [(idx, Video(title, artist, vid_id, fav, archived))
              for (idx, title, artist, vid_id, fav, archived) in data]
    for idx, (_, video) in enumerate(videos):
        print(f"{idx:4} {video}")

    db_id, video = videos[int(input("Choose: "))]
    print(video)
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

    db = sqlite3.connect(DB_FILENAME)
    cursor = db.cursor()
    command = f"""
        UPDATE asmr
        SET {','.join(updates)}
        WHERE id={db_id}
    """
    cursor.execute(command)
    db.commit()


@cli.command(short_help="View list of videos")
@click.argument('query', nargs=-1)
@click.option('-f', '--only-favourites', is_flag=True, default=False)
@click.option('-a', '--with-archived', is_flag=True, default=False)
def view(query, only_favourites, with_archived):
    """List videos, optionally filtered by query or favourites only"""
    query = ' '.join(query).lower()
    fav = "AND fav = 1" if only_favourites else ""
    archived = "AND archived = 0" if not with_archived else ""
    sql_query = f"""
        select * from asmr
        where (title like '%{query}%' or artist like '%{query}%')
            {fav} {archived}
        ORDER BY artist, fav DESC, title
    """
    _, data = execute_select(sql_query)
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
    sql_query = f"""
        select * from asmr
        where (title like '%{query}%' or artist like '%{query}%')
            {fav} {archived}
    """
    _, data = execute_select(sql_query)
    videos = [(idx, Video(title, artist, vid_id, fav, archived))
              for (idx, title, artist, vid_id, fav, archived) in data]
    choice = choose(videos, random)
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
        """Search for query in title or artist"""
        query = query.lower()
        return query in self.title.lower() or query in self.artist.lower()

    def __str__(self):
        """Prettyprint"""
        fav = "F" if self.fav else "."
        arc = "@" if self.archived else "."
        return f"{fav} {arc} {self.artist:20s}{self.title}"

    def open(self):
        """Generate URL from video id and open in browser"""
        url = f"https://www.youtube.com/watch?v={self.vid_id}"
        webbrowser.open(url)


def display(entries):
    """For every asmr entry, display it's index and a pretty printed title"""
    title = f"   # F A {'ARTIST'.ljust(20)}TITLE"
    print(title)
    print("-"*(len(title)+20))
    for idx, (_, entry) in enumerate(entries):
        print(f"{idx:4} {entry}")


def choose(list, random=False):
    """Choose an entry from a list, or get a random one."""
    if not list:
        raise Exception("List is empty")
    if random:
        return random_choice(list)[1]
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
    cli()
except Exception as E:
    print(E)
