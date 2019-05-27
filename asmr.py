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
from functools import lru_cache

from docopt import docopt


FILENAME = str((Path(os.environ["DATADIR"]) / "asmr.json").resolve())


@lru_cache(4096)
def levenshtein(a, b):
    """Compute levenshtein edit distance between two strings"""
    if not a or not b:
        return max(len(a), len(b))
    if a[0] == b[0]:
        return levenshtein(a[1:], b[1:])
    return 1 + min(
        levenshtein(a[1:], b), levenshtein(a, b[1:]), levenshtein(a[1:], b[1:])
    )


def check_for_similar_artist(artists):
    new_artist = input("Artist: ")
    distances = {(artist, levenshtein(new_artist, artist)) for artist in artists}
    similar = {artist for (artist, distance) in distances if distance < 3}
    exact = {artist for (artist, distance) in distances if distance == 0}
    if similar and not exact:
        print("Similar artists")
        for i, artist in enumerate(similar):
            print(f"{i}\t{artist}")
        video = int(input(f"Artist, or -1 to use '{new_artist}': "))
        return new_artist if video == -1 else similar[video]
    return new_artist


def urlify(url):
    if not url.startswith("http") and not url.startswith("www"):
        return f"https://www.youtube.com/watch?v={url}"
    return url


def add(*, videos):
    """Give the user inputs to add a new video to the ASMRFILE"""
    artists = [v["artist"] for v in videos]
    artist = check_for_similar_artist(artists)
    title = input("Title: ")
    url = urlify(input("Video ID: "))
    videos.append({"title": title, "artist": artist, "url": url})
    return videos


def modify(*, videos, mask):
    """Modify an existing video's metadata"""
    choices = [int(c) for c in input("Choice(s): ").replace(" ", ",").split(",")
               if int(c) in mask]
    print("\nEnter new values, or press enter to keep current value")

    def prompt_or_stay_same(prompt, current):
        val = input(f"\t{prompt} ({current}): ")
        if not val:
            return current
        return val

    for idx in choices:
        artists = [v["artist"] for v in videos]
        videos[idx]["artist"] = check_for_similar_artist(artists)
        videos[idx]["title"] = prompt_or_stay_same("Title", videos[idx]["title"])
        videos[idx]["url"] = urlify(prompt_or_stay_same("URL", videos[idx]["url"]))
        videos[idx]["broken"] = prompt_or_stay_same(
            "Broken?", videos[idx]["broken"]
        )
    return videos


def delete(*, videos, mask):
    """Delete videos"""
    choices = [int(c) for c in input("Choice(s): ").replace(" ", ",").split(",")
               if int(c) in mask]
    for idx in sorted(choices, reverse=True):
        del videos[video]
    return videos


def play(*, videos, mask, random):
    """Play a video (optionally filtered)"""
    choices = [random_choice(mask)]
    if not random:
        choices = [int(c) for c in input("Choice(s): ").replace(" ", ",").split(",")
                   if int(c) in mask]
    for idx in choices:
        video = videos[idx]
        print(f"{video['title']} ~~~ {video['artist']}")
        webbrowser.open(video["url"])
    return videos


def main():
    """Run asmr video util"""
    args = docopt(__doc__)
    query = " ".join(args["<query>"]).lower()
    videos = json.load(open(FILENAME, "r"))
    mask = [i for i, v in enumerate(videos)
            if query in v['title'].lower() or query in v['artist'].lower()]
    is_random=args['--random']

    title = f"   # {'ARTIST'.ljust(20)}TITLE"
    print(title)
    print("-" * (len(title) + 20))
    for idx, video in enumerate(videos):
        if idx in mask:
            print(f"{idx:4}) {video['artist']:20s}{video['title']}")
    print()

    if args['play']:
        new_videos = play(videos=videos[:], mask=mask, random=is_random)
    elif args['modify']:
        new_videos = modify(videos=videos[:], mask=mask)
    elif args['delete']:
        new_videos = delete(videos=videos[:], mask=mask)
    elif args['add']:
        new_videos = add(videos=videos[:])
    else: # args['view']
        # The 'view' command is basically a NOOP since main always displays videos
        new_videos = videos
    if not new_videos:
        print("Something went wrong. No videos")
        new_videos = videos
    sorted_videos = sorted(new_videos, key=lambda x: x["artist"])
    json.dump(sorted_videos, open(FILENAME, "w"), indent=2)


if __name__ == "__main__":
    main()
