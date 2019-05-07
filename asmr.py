#!/usr/bin/env python3
"""ASMR video management

Usage:
    asmr play [-far] [<query>]...
    asmr view [-fa] [<query>]...
    asmr modify [<query>]...
    asmr add

Commands:
    play    Play a video matching query
    view    List all videos matching query
    modify  Change metadata of an existing video
    add     Add a new video to the database

Options:
    -f --favourites      Display only favourites      [default: False]
    -a --with-archived   Also display archived videos [default: False]
    -r --random          Choose a random video        [default: False]
"""
import os
import re
import sqlite3
import webbrowser
from collections import namedtuple
from pathlib import Path
from random import choice as random_choice

from docopt import docopt


Video = namedtuple("Video", "title artist vid_id fav archived")
DB_FILENAME = str((Path(os.environ["DATADIR"]) / "data.db").resolve())


def format_video(video):
    """Prettyprint a Video"""
    fav = "F" if video.fav else "."
    arc = "@" if video.archived else "."
    return f"{fav} {arc} {video.artist:20s}{video.title}"


def display(entries):
    """For every asmr entry, display it's index and a pretty printed title"""
    title = f"   # F A {'ARTIST'.ljust(20)}TITLE"
    print(title)
    print("-" * (len(title) + 20))
    for idx, entry in enumerate(entries):
        print(f"{idx:4} {format_video(entry)}")


def choose(entries, random=False):
    """Choose an entry from a entries, or get a random one."""
    if not entries:
        raise Exception("choose: Can't choose from an empty video list.")
    if random:
        return random_choice(entries)
    if len(entries) == 1:
        return entries
    display(entries)
    response = input("Choose: ")
    # Split optionally on ",", to allow entry of multiple choices
    choice = [int(i.strip()) for i in response.split(",")]
    return [entries[c] for c in choice]


def select_videos(only_favourites, with_archived, query):
    """Run a database query for videos"""
    fav = "AND fav = 1" if only_favourites else ""
    archived = "AND archived = 0" if not with_archived else ""
    database = sqlite3.connect(DB_FILENAME)
    cursor = database.cursor()
    cursor.execute(
        f"""
        select * from asmr
        where (title like '%{query}%' or artist like '%{query}%')
            {fav} {archived}
        ORDER BY artist, fav DESC, title"""
    )
    data = cursor.fetchall()
    database.close()
    return [Video(*d) for d in data]


def add(**kwargs):
    """Give the user inputs to add a new video to the ASMRFILE"""
    artist = input("Artist: ")
    title = input("Title: ")
    vid = input("Video ID: ")
    fav = 1 if input("Fav [y/n]: ")[0] in ["Y", "y"] else 0

    if vid.startswith("www.") or vid.startswith("http"):
        match = re.search(".*?video=(.{11}).*", vid)
        if match:
            vid = match.group(1)
    if not vid or len(vid) != 11:
        raise Exception("add: Could not parse video id")

    database = sqlite3.connect(DB_FILENAME)
    cursor = database.cursor()
    cursor.execute(
        f"""
        INSERT INTO asmr(title, artist, hash, fav, archived)
        VALUES ( '{title}', '{artist}', '{vid}', '{fav}', '0' )
    """
    )
    database.commit()
    database.close()


def modify(*, query, **kwargs):
    """Modify an existing video's metadata"""
    query = " ".join(query).lower()
    only_favourites, with_archived = False, True
    videos = select_videos(only_favourites, with_archived, query)
    video = choose(videos, False)
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
        WHERE artist={video.artist} and title={video.title}
    """
    cursor.execute(command)
    database.commit()


def view(*, query, only_favourites, with_archived, **kwargs):
    """List videos, optionally filtered by query or favourites only"""
    query = " ".join(query).lower()
    videos = select_videos(only_favourites, with_archived, query)
    display(videos)


def play(*, query, random, only_favourites, with_archived):
    """Play a video (optionally filtered)"""
    query = " ".join(query).lower()
    videos = select_videos(only_favourites, with_archived, query)
    choice = choose(videos, random)
    for video in choice:
        print(format_video(video))
        url = f"https://www.youtube.com/watch?v={video.vid_id}"
        webbrowser.open(url)


def main():
    """Run asmr video util"""
    args = docopt(__doc__)
    commands = [("play", play), ("view", view), ("modify", modify), ("add", add)]
    # Due to the way docopt works, we should _always_ have one of the above commands
    # by the time we reach this point, so it's save to just take the 0th
    # Also, only one command should be available, so the list should be length 1.
    command = [func for (funcname, func) in commands if args[funcname]][0]
    command(
        query=args["<query>"],
        random=args["--random"],
        only_favourites=args["--favourites"],
        with_archived=args["--with-archived"],
    )


if __name__ == "__main__":
    main()
