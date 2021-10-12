#!/usr/bin/env python3
import pinboard
from collections import Counter

token = open('/home/cdavison/.pinboard').read().strip()
pb = pinboard.Pinboard(token)
posts = pb.posts.all()
towatch = [p for p in posts if 'video' in p.tags and p.toread]

c = Counter()
for bookmark in towatch:
    c.update(bookmark.tags)

tags = [f'{a} ({b})' for a, b in c.most_common(10)]
print(len(towatch), 'videos to watch')
print(f'{len(c.keys())} unique tags')
print(f'{len(tags)} most common tags: ', ', '.join(tags))
