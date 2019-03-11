"""
## Views

- [`/` - view books (with optional query params)](/)
    - `r=0|1` Books that have been read
    - `genre=<GENRE>`
    - `s=<STATUS>`
    - `query=<QUERY>` - Search in title and author
- [`/read`](/read)
- [`/genres`](/genres)
- [`/buy`](/buy)
- [`/wip`](/wip)
- [Next books?](/?status=Unread)

## Utility categories

- [Books to revisit/re-read](/?status=Re-Read)
- [Possible statuses of books](/statuses)
- `/help` - this view

## Modification

- [`/add`](/add) - Add a new purchase
"""
import json
import os
import pandas as pd
import sys
from collections import defaultdict
from itertools import groupby
from textwrap import dedent

import dateutil
from flask import Flask, render_template, request
from markdown import markdown

app = Flask(__name__)

fn = "/Users/davison/Dropbox/data/reading-list.json"

def get_books():
    books = json.load(open(fn))
    tidied = []
    for b in books:
        b['Read'] = '' if not b['Read'] else b['Read']
        b['Author'] = '' if not b['Author'] else b['Author']
        tidied.append(b)
    return tidied


def get_filtered_books(request):
    books = get_books()
    genre=request.args.get('genre', '').lower()
    status=request.args.get('status', '').lower()
    read=request.args.get('read', '').lower()
    query=request.args.get('query', '').lower()
    if genre:
        books = [b for b in books if b['Genre'].lower().startswith(genre)]
    if read:
        books = [b for b in books if b['Read']]
    if status:
        books = [b for b in books if b['Status'].lower() == status]
    if query:
        books = [b for b in books if any(query in b['Author'], query in b['Title'])]
    return books


@app.route("/h")
@app.route("/help")
def help():
    content = markdown(dedent(__doc__))
    return render_template("raw.html", content=content, title="Help")


@app.route("/genres")
def genres():
    genres = sorted(set(b['Genre'] for b in get_books()))
    no_space = lambda x: x.replace(' ', '%20')
    genres_as_list = "\n".join([f"- [{c}](/?genre={no_space(c)})" for c in genres])
    formatted = markdown(dedent(genres_as_list))
    return render_template("raw.html", content=formatted, title="genres")


@app.route("/statuses")
def statuses():
    statuses = sorted(set(b['Status'] for b in get_books()))
    no_space = lambda x: x.replace(' ', '%20')
    statuses_as_list = "\n".join([f"- [{c}](/?status={no_space(c)})" for c in statuses])
    formatted = markdown(dedent(statuses_as_list))
    return render_template("raw.html", content=formatted, title="Statuses")


@app.route("/buy")
def buy():
    books = [b for b in get_filtered_books(request) if b['Status'] == 'Buy']
    return render_template("index.html", books=books)


@app.route("/wip")
def wip():
    books = [b for b in get_filtered_books(request) if b['Status'] == 'WIP']
    return render_template("index.html", books=books)


@app.route("/read")
def read():
    books_by_date = defaultdict(list)
    for b in get_books():
        if not b['Read']:
            continue
        b['Read_dt'] = dateutil.parser.parse(b['Read'])
        fmtd = b['Read_dt'].strftime("%Y-%m")
        books_by_date[fmtd].append(b)
    out = ""
    for date in sorted(books_by_date.keys()):
        books = books_by_date[date]
        out += f"\n\n## {date}\n"
        out += "\n".join(f"- **{book['Title']}** by *{book['Author']}* ({book['Genre']}))"
                for book in sorted(books, key=lambda x: x['Title']))
        out += "<br>"
    print(out)
    formatted = markdown(dedent(out))
    return render_template("raw.html", content=formatted, title="Books read")


@app.route("/")
def filter():
    return render_template("index.html", books=get_filtered_books(request))


@app.route("/new", methods=['POST'])
def new():
    books = get_books()
    books.append({
        'Title': request.form['title'],
        'Author': request.form['author'],
        'Genre': request.form['genre'],
        'Status': request.form['status'],
        'Read': request.form['read']
    })
    json.dump(books, open(fn, 'w'), indent=2)
    return render_template("index.html", books=books[-10:], extra_pre=f"Added: {request.form['title']} by {request.form['author']}")


@app.route("/add")
def add():
    return render_template("add.html", title="Add a book")
