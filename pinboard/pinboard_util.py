#!/usr/bin/env python3
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from wordcloud import WordCloud
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pinboard
import seaborn as sns
import sys

def bookmarkhash(self):
    return self.url.__hash__()

def bookmark_show(self):
    return f"{self.description}\n{self.url}\n{' '.join('#' + t for t in self.tags)}"

cache = None
cache_path = Path('~/.pinboard_cache').expanduser()
pbutil_verbose = True
pinboard.Bookmark.__hash__ = bookmarkhash
pinboard.Bookmark.__str__ = bookmark_show

def refresh_posts(if_older_than=timedelta(minutes=30), force=False):
    global cache
    global pbutil_verbose
    if cache_path.exists():
        cache = pickle.load(open(cache_path, 'rb'))
    else:
        cache = {'posts': [], 'last_updated': None}
        pickle.dump(cache, open(cache_path, 'wb'))

    if not cache['posts'] or (datetime.now() - cache['last_updated']) > if_older_than or force:
        if pbutil_verbose:
            print("REFRESHING POSTS")
        token = Path("~/.pinboard").expanduser().read_text().strip()
        pb = pinboard.Pinboard(token)
        cache['posts'] = pb.posts.all()
        cache['last_updated'] = datetime.now()
        if pbutil_verbose:
            print("New post refresh threshold:", cache['last_updated'].strftime("%H:%M"))
        pickle.dump(cache, open(cache_path, 'wb'))
    else:
        if pbutil_verbose:
            print("USING `OLD` POSTS TILL", (cache['last_updated'] + if_older_than).strftime("%H:%M"))

def related_tags(posts):
    collocated_tags = defaultdict(Counter)

    for bookmark in posts:
        for tag in bookmark.tags:
            collocated_tags[tag].update(set(bookmark.tags) - set([tag]))
    return collocated_tags


def tag_counts_to_word_cloud(counted_tags, excludes=None):
    repeated_tags = [tag for tag, count in counted_tags.items() for _ in range(count)]
    if excludes and isinstance(excludes, list):
        repeated_tags = [tag for tag in repeated_tags if tag not in excludes]

    np.random.shuffle(repeated_tags)

    wordcloud = WordCloud(width = 1200, height = 1200,
                    background_color ='white',
                    min_font_size = 10).generate(" ".join(repeated_tags))

    # plot the WordCloud image
    _ = plt.figure(figsize = (12, 12), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)


def heatmap_of_related_tags(tag, posts):
    related = related_tags(posts)
    tags_to_consider = list(related[tag].keys()) + [tag]
    print(f"{len(tags_to_consider)} tags related to '{tag}'\n")
    grid = np.zeros((len(tags_to_consider), len(tags_to_consider)))

    for tag_a in tags_to_consider:
        for tag_b in (set(tags_to_consider) - set([tag])):
            n = sum([1 for p in posts if tag in p.tags and tag_a in p.tags and tag_b in p.tags])
            idx_a = tags_to_consider.index(tag_a)
            idx_b = tags_to_consider.index(tag_b)
            if tag_a == tag_b:
                grid[idx_a, idx_b] = -1
            else:
                grid[idx_a, idx_b] += n

    grid_df = pd.DataFrame(grid, columns=tags_to_consider)
    grid_df.index = tags_to_consider
    _, ax = plt.subplots(1, figsize=(20, 15))
    sns.heatmap(grid_df, ax=ax)
    plt.title(f'Collocation of tags related to {tag}')
    plt.tight_layout()


class Filter:
    def __init__(self, query):
        self.tags_include = []
        self.tags_exclude = []
        self.words_include = []
        self.words_exclude = []
        for p in query:
            if p.startswith('-t:'):
                self.tags_exclude.append(p[3:])
            elif p.startswith('-#'):
                self.tags_exclude.append(p[2:])
            elif p.startswith('t:'):
                self.tags_include.append(p[2:])
            elif p.startswith('#'):
                self.tags_include.append(p[1:])
                self.words_include.append(p[1:])
            elif p.startswith('-'):
                self.words_exclude.append(p[1:])
            else:
                self.words_include.append(p)

    def is_match(self, bookmark):
        d = bookmark.description.lower()
        u = bookmark.url
        t = bookmark.tags
        has_words = not self.words_include or all(w in d or w in u for w in self.words_include)
        has_no_bad_words = not self.words_exclude or not any(w in d or w in u for w in self.words_exclude)
        has_tags = not self.tags_include or all(w in t for w in self.tags_include)
        has_no_bad_tags = not self.tags_exclude or not any(w in t for w in self.tags_exclude)
        return all([has_words, has_tags, has_no_bad_words, has_no_bad_tags])


if __name__ == '__main__':
    from argparse import ArgumentParser
    from typing import List
    pbutil_verbose=False

    parser = ArgumentParser()
    commands = parser.add_subparsers(title='command', dest='command', required=True)
    tags = commands.add_parser('tags', aliases=['t'])
    posts = commands.add_parser('posts', aliases=['p'])

    tags.add_argument("query", nargs="*", type=str)
    tags.add_argument("-u", "--unread", action='store_true')
    tags.add_argument("-r", "--refresh", action='store_true')

    posts.add_argument("query", nargs="*", type=str)
    posts.add_argument("-u", "--unread", action='store_true')
    posts.add_argument("-r", "--refresh", action='store_true')

    args = parser.parse_args()

    refresh_posts(force=args.refresh)
    post_filter = Filter(args.query)

    posts = cache['posts']
    if args.unread:
        posts = (p for p in posts if p.toread)
    posts = [p for p in posts if post_filter.is_match(p)]
    if not posts:
        print('NO MATCHING POSTS')
        sys.exit(1)

    if args.command in ['tags', 't']:
        counts = Counter()
        for bm in posts:
            counts.update(bm.tags)
        for k, v in counts.most_common(30):
            print(v, k)
    elif args.command in ['posts', 'p']:
        n = 10
        chosen = set(np.random.choice(posts, n))
        if len(chosen) < n:
            print(f"Asked for {n}; found {len(chosen)}")
        for bm in chosen:
            print(bm)
            print()
