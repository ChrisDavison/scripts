#!/usr/bin/env python3
from enum import Enum
import json
import os
import random
import sys
import webbrowser


class Errors(Enum):
    none = 0
    no_vid = 1
    short_vid_hash = 2
    vid_already_exists = 3


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


class asmr_vids:
    def __init__(self, filename):
        self.entries = json.load(open(filename, encoding='utf8'))
        self.filtered = self.entries
        self.choice = None


    def display(self):
        for i, entry in enumerate(self.filtered):
            print(f"{i:4} {self[i]}")


    def choose(self):
        self.display()
        choice = int(input("Which one?: "))
        self.choice = self.filtered[choice]


    def random(self):
        N = len(self.filtered)
        self.choice = self.filtered[random.randint(0, N)]


    def filter(self, query):
        q = query.lower()
        self.filtered = [e for e in self.entries
                         if q in e['artist'].lower() or q in e['title'].lower()]
        if not self.filtered:
            print("No matching videos")
            sys.exit(Errors.no_vid)


    def __getitem__(self, index):
        e = self.filtered[index]
        s = style.BOLD if e['fav'] else ''
        return f"{s}{e['artist']:20}{e['title']}{style.END}"


    def __str__(self):
        if self.choice:
            s = style.BOLD if self.choice['fav'] else ''
            return f"{s}{self.choice['artist']:20}{self.choice['title']}{style.END}"
        else:
            return "No matching video."


    def open(self):
        if self.choice:
            print(self)
            url = f"https://www.youtube.com/watch?v={self.choice['hash']}"
            webbrowser.open(url)
            sys.exit(Errors.none)
        else:
            print("No matching video")
            sys.exit(Errors.no_vid)


    def add(self, artist, title, fav, hashid):
        any_matching = [i for i, e in enumerate(self.entries)
                        if hashid == e['hash']]
        if any_matching:
            print(f"Video already exists: {self[any_matching[0]]}")
            sys.exit(Errors.vid_already_exists)
        else:
            self.entries.append({'artist': artist, 'title': title, 'fav': fav, 'hash': hashid})


def main():
    filename = os.path.expanduser('~/Dropbox/asmr.json')
    vids = asmr_vids(filename)
    flags = [a for a in sys.argv[1:] if a.startswith('-')]
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    add_an_entry = '-a' in flags
    just_pick_random = '-r' in flags
    just_list = '-l' in flags
    if add_an_entry:
        artist = input("Artist: ")
        title = input("Title: ")
        fav = input("Fav [y/n]: ").lower()
        vid = input("Video ID: ")
        if len(vid) < 11:
            print("Video hash must be >= 11 characters")
            sys.exit(Errors.short_vid_hash)
        vids.add(artist, title, True if fav == 'y' else False, vid)
        print(vids[len(vids.entries)-1])
        json.dump(vids.entries, open(filename, 'w', encoding='utf8'), indent=2)
    else:
        query = ' '.join(args)
        if query:
            vids.filter(query)
        if just_pick_random:
            vids.random()
        if not just_pick_random:
            vids.choose()
        vids.open()


if __name__ == "__main__":
    main()


