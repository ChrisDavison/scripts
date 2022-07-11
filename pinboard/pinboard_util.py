from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pinboard
import seaborn as sns

def bookmarkhash(self):
    return self.url.__hash__()

def bookmark_show(self):
    return f"{self.description}\n{self.url}\n{' '.join('#' + t for t in self.tags)}"

posts = []
last_updated = None

pinboard.Bookmark.__hash__ = bookmarkhash
pinboard.Bookmark.__str__ = bookmark_show

def refresh_posts(if_older_than=timedelta(minutes=30), force=False):
    global posts
    global last_updated
    if not posts or (datetime.now() - last_updated) > if_older_than or force:
        print("REFRESHING POSTS")
        token = Path("~/.pinboard").expanduser().read_text().strip()
        pb = pinboard.Pinboard(token)
        posts = pb.posts.all()
        last_updated = datetime.now()
        print("New post refresh threshold:", last_updated.strftime("%H:%M"))
    else:
        print("USING `OLD` POSTS TILL", (last_updated + if_older_than).strftime("%H:%M"))
    return posts


def fuzzy_find_posts(which='all', *, terms, excluded_tags=[]):
    matches = []

    def matches_terms(terms, post):
        for t in terms:
            lower_tags = map(lambda x: x.lower(), post.tags)
            if not any([t in lower_tags, t in post.description.lower(), t in post.url]):
                return False
        return True

    refresh_posts()
    local_posts = posts
    if which == 'unread':
        local_posts = [p for p in local_posts if p.toread]
    for p in local_posts:
        if excluded_tags and any(tag in excluded_tags for tag in p.tags):
            continue
        if matches_terms(terms, p):
            matches.append(p)

    if not matches:
        print("NO MATCHES")
    return matches

def count_tags(which='all', excludes=None, exclude_entire_post=True):
    refresh_posts()
    local_posts = posts
    if which == 'unread':
        local_posts = [p for p in local_posts if p.toread]
    counts = Counter()
    n_matching = 0
    for bookmark in local_posts:
        tags = bookmark.tags
        if excludes:
            if exclude_entire_post and any(tag in tags for tag in excludes):
                continue
            else:
                tags = [tag for tag in tags if tag not in excludes]
        counts.update(tags)
        n_matching += 1
    print(f"{n_matching} matching posts")
    return counts

def count_tags_matching(which='all', includes=None, excludes=None, exclude_entire_post=True):
    refresh_posts()
    local_posts = fuzzy_find_posts(which, terms=includes, excluded_tags=excludes)
    counts = Counter()
    n_matching = 0
    for bookmark in local_posts:
        tags = bookmark.tags
        if excludes:
            if exclude_entire_post and any(tag in tags for tag in excludes):
                continue
            else:
                tags = [tag for tag in tags if tag not in excludes]
        counts.update(tags)
        n_matching += 1
    print(f"{n_matching} matching posts")
    return counts

def related_tags(which='all'):
    refresh_posts()

    collocated_tags = defaultdict(Counter)
    local_posts = posts

    if which == 'unread':
        local_posts = [p for p in local_posts if p.toread]
    for bookmark in local_posts:
        for tag in bookmark.tags:
            collocated_tags[tag].update(set(bookmark.tags) - set([tag]))
    return collocated_tags

def display_n_fuzzy_matches(which='all', n=10, terms=[], excluded_tags=[]):
    found = fuzzy_find_posts(which, terms=terms, excluded_tags=excluded_tags)
    if not found:
        print("No matches.")
        return
    chosen = set(np.random.choice(found, n))
    if len(chosen) < n:
        print(f"Asked for {n}; found {len(chosen)}")
    for bm in chosen:
        print(bm)
        print()


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

def heatmap_of_related_tags(tag, which='all', excludes=[]):
    related = related_tags(which)
    tags_to_consider = list(related[tag].keys()) + [tag]
    if excludes:
        tags_to_consider = [t for t in tags_to_consider if t not in excludes]
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
