#!/usr/bin/env python3
"""ASMR video management

Usage:
    asmr play [-r] [<query>]...
    asmr view [<query>]...
    asmr modify [<query>]...
    asmr delete [<query>]...
    asmr add

Commands:
    play    Play a video matching query
    view    List all videos matching query
    modify  Change metadata of an existing video
    add     Add a new video to the database
    delete  Delete a video

Options:
    -r --random          Choose a random video        [default: False]
"""
import os
import json
import re
import webbrowser
from pathlib import Path
from random import choice as random_choice

from docopt import docopt


FILENAME = str((Path(os.environ["DATADIR"]) / "asmr.json").resolve())


def write_sorted_videos(videos):
    sorted_videos = sorted(videos, key=lambda x: x['artist'])
    json.dump(sorted_videos, open(FILENAME, 'w'), indent=2)


def read_videos():
    return json.load(open(FILENAME, 'r'))


def contains(v, query):
    query = query.lower()
    return query in v['artist'].lower() or query in v['title'].lower()


def new_video():
    title = input("Title: ")
    artist = input("Artist: ")
    url = input("URL: ")
    if not (url.startswith('http') or url.startswith('www.')):
        url = f"https://www.youtube.com/watch?v={url}"
    return {'title': title, 'artist': artist, 'url': url}


def format_video(video):
    """Prettyprint a Video"""
    return f"{video['artist']:20s}{video['title']}"


def display(entries):
    """For every asmr entry, display it's index and a pretty printed title"""
    title = f"   # {'ARTIST'.ljust(20)}TITLE"
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


def select_videos(query):
    """Load and filter videos"""
    videos = read_videos()
    return [v for v in videos if contains(v, query)]


def urlify(url):
    if not url.startswith('http') and not url.startswith('www'):
        return f"https://www.youtube.com/watch?v={url}"
    return url


def add(**kwargs):
    """Give the user inputs to add a new video to the ASMRFILE"""
    artist = input("Artist: ")
    title = input("Title: ")
    url= urlify(input("Video ID: "))

    videos = read_videos()
    videos.append({'title': title, 'artist': artist, 'url': url})
    write_sorted_videos(videos)



def modify(*, query, **kwargs):
    """Modify an existing video's metadata"""

    query = " ".join(query).lower()
    videos = read_videos()
    for i, video in enumerate(videos):
        if contains(video, query):
            print(f"{i:5d}\t{format_video(video)}")
    choice = int(input("Choice: "))

    print("\nEnter new values, or press enter to keep current value")

    def prompt_or_stay_same(prompt, current):
        val = input(f"\t{prompt} ({current}): ")
        if not val:
            return current
        return val

    videos[choice]['artist'] = prompt_or_stay_same("Artist", videos[choice]['artist'])
    videos[choice]['title'] = prompt_or_stay_same("Title", videos[choice]['title'])
    videos[choice]['url'] = urlify(prompt_or_stay_same("URL", videos[choice]['url']))
    videos[choice]['broken'] = prompt_or_stay_same("Broken?", videos[choice]['broken'])
    write_sorted_videos(videos)


def delete(*, query, **kwargs):
    """Delete a video"""
    query = " ".join(query).lower()
    videos = read_videos()
    for i, video in enumerate(videos):
        if contains(video, query):
            print(f"{i:5d}\t{format_video(video)}")
    choice = int(input("Choice: "))
    if choice in range(len(videos)):
        del videos[choice]
    write_sorted_videos(videos)


def view(*, query, **kwargs):
    """List videos, optionally filtered by query"""
    query = " ".join(query).lower()
    videos = select_videos(query)
    display(videos)


def play(*, query, random):
    """Play a video (optionally filtered)"""
    query = " ".join(query).lower()
    videos = select_videos(query)
    choice = choose(videos, random)
    for video in choice:
        print(format_video(video))
        webbrowser.open(video['url'])


def main():
    """Run asmr video util"""
    args = docopt(__doc__)
    commands = [("play", play), ("view", view), ("modify", modify), ("add", add), ("delete", delete)]
    # Due to the way docopt works, we should _always_ have one of the above commands
    # by the time we reach this point, so it's save to just take the 0th
    # Also, only one command should be available, so the list should be length 1.
    command = [func for (funcname, func) in commands if args[funcname]][0]
    command(
        query=args["<query>"],
        random=args["--random"]
    )


if __name__ == "__main__":
    main()
