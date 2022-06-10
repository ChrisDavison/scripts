#!/usr/bin/env python3
import pinboard
from collections import Counter, defaultdict
from pathlib import Path
import sys
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-n", default=10, type=int)
    parser.add_argument("--excludes", nargs="+", type=str)
    args = parser.parse_args()

    token = Path("~/.pinboard").expanduser().read_text().strip()
    pb = pinboard.Pinboard(token)
    posts = pb.posts.all()
    towatch = [p for p in posts if p.toread]

    c = Counter()
    collocated_tags = defaultdict(set)
    for bookmark in towatch:
        c.update(bookmark.tags)
        for tag in bookmark.tags:
            tags_without_tag = set(bookmark.tags) - set([tag])
            collocated_tags[tag].update(tags_without_tag)

    for e in args.excludes:
        del c[e]
    tags = [(a, b) for a, b in c.most_common(args.n)]

    print(f"{len(towatch)} unread bookmarks with {len(c.keys())} unique tags")
    print()
    excludestr = " (excluding " + ", ".join(args.excludes) + ")" if args.excludes else ""
    print(f'{len(tags)} most common tags{excludestr}:')
    for tag, tagcount in tags:
        related = ", ".join(collocated_tags[tag])
        if len(related) > 60:
            related = related[:60] + "..."
        print(f"- {tagcount:4d} x {tag:<30} ({related})")
