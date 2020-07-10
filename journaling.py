#!/usr/bin/env python3
"""journaling: command-line journaling, to json

Usage:
    journaling.py add
    journaling.py search <text>...
    journaling.py search -t <tags>...
    journaling.py list|ls [dates|tags]
    journaling.py show [<date>]
    journaling.py markdown
"""
import datetime
import json
import textwrap
from pathlib import Path

from docopt import docopt


def get_tagmap(journals):
    tags = {}
    for date, entry in journals.items():
        for tag in entry['tags']:
            if tag in tags:
                tags[tag].append(date)
            else:
                tags[tag] = [date]
    return tags


def search_tags(journals, tagmap):
    tags = get_tagmap(journals)
    for tag in tags:
        matching = tagmap.get(tag, [])
        print('Entries matching tag `{}`'.format(tag))
        for entry in matching:
            print('    {}'.format(entry))


def matches_all(words, text):
    text = text.lower()
    for word in words:
        if word.lower() not in text:
            return False
    return True


def search_text(words, journals):
    print('Searching for entries that matches all of:')
    print("    '{}'".format(', '.join(words)))
    for date, entry in journals.items():
        if matches_all(words, entry['text']):
            print(date)


def wrap_and_listify(entries):
    spacer = lambda i: '-' if i == 0 else ' '
    wrapped = [textwrap.wrap(e, width=68) for e in entries]
    wrapped = [f"{spacer(i)}   {l}"
               for lines in wrapped 
               for i, l in enumerate(lines)]
    return '\n'.join(wrapped)


def list(showdates, showtags, journals):
    if args['dates'] or not showtags:
        print('dates: ', ', '.join(journals.keys()))
    if args['tags'] or not showdates:
        print('tags: ', ', '.join(get_tagmap(journals)))


def add(journals):
    today = str(datetime.date.today())
    print("Adding to today ({})".format(today))
    tags = input('Tags: ').strip().split(' ')
    text = input('Text: ').strip()
    if today in journals:
        if tags != ['']:
            journals[today]['tags'].extend(tags)
        if text:
            journals[today]['text'].append(text)
    else:
        journals[today] = {'tags': tags, 'text': [text]}
    json.dump(journals, open(filename, 'w'), indent=2)


def show(date, journals, tags_on_sameline=True):
    if date and date in journals:
        entry = journals[date]
        date = date
    else:
        print('Showing last journal')
        print()
        date = sorted(journal.keys())[-1]
        entry = journals[date]
    tagstr = ''
    if entry['tags']:
        if tags_on_sameline:
            tagstr = '@{' + ', '.join(entry['tags']) + '}'
        else:
            tagstr = '\n\n' + ' '.join('@'+e for e in entry['tags']) + '\n'
    print(date, tagstr)
    print(wrap_and_listify(entry['text']))


def as_markdown(journals):
    keys = sorted(journals.keys())
    for key in keys:
        print('#', end=' ')
        show(key, journals, tags_on_sameline=False)


if __name__ == "__main__":
    args = docopt(__doc__)
    filename = Path("~/Dropbox/journal.json").expanduser()
    journal = json.load(open(filename))
    if args['search'] and args['-t']:
        search_tags(args['<tags>'], tags)
    elif args['search']:
        search_text(args['<text>'], journal)
    elif args['list'] or args['ls']:
        list(args['dates'], args['tags'], journal)
    elif args['show']:
        show(args['<date>'], journal)
    elif args['markdown']:
        as_markdown(journal)
    else:
        add(journal) 
