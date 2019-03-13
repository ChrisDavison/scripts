"""## Books

- [`/books/` (with optional query params)](/books/)
    - `r=0|1` Books that have been read
    - `genre=<GENRE>`
    - `s=<STATUS>`
    - `query=<QUERY>` - Search in title and author
- [`/books/read`](/books/read)
- [`/books/genres`](/books/genres)
- [`/books/buy`](/books/buy)
- [`/books/wip`](/books/wip)
- [Books unread](/books/?status=Unread)
- [Books to revisit/re-read](/books/?status=Re-Read)
- [`/books/statuses` (reading)](/books/statuses)
- [`/books/help`](/books/help) for this view
"""
import json
import os
import pandas as pd
import sys
from collections import defaultdict
from itertools import groupby
from textwrap import dedent

import dateutil
from flask import Flask, render_template, request, Blueprint
from markdown import markdown

books = Blueprint('books', __name__, template_folder='templates')

fn = os.path.join(os.environ["DATADIR"], "reading-list.json")

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
    return sorted(books, key=lambda x: x['Read'])


@books.route("/books/help")
def bookhelp():
    content = markdown(dedent(__doc__))
    return render_template("raw.html", content=content, title="Help")


@books.route("/books/genres")
def genres():
    genres = sorted(set(b['Genre'] for b in get_books()))
    no_space = lambda x: x.replace(' ', '%20')
    genres_as_list = "\n".join([f"- [{c}](/books/?genre={no_space(c)})" for c in genres])
    formatted = markdown(dedent(genres_as_list))
    return render_template("raw.html", content=formatted, title="genres")


@books.route("/books/statuses")
def statuses():
    statuses = sorted(set(b['Status'] for b in get_books()))
    no_space = lambda x: x.replace(' ', '%20')
    statuses_as_list = "\n".join([f"- [{c}](/books/?status={no_space(c)})" for c in statuses])
    formatted = markdown(dedent(statuses_as_list))
    return render_template("raw.html", content=formatted, title="Statuses")


@books.route("/books/buy")
def buy():
    books = [b for b in get_filtered_books(request) if b['Status'] == 'Buy']
    return render_template("books.html", books=books)


@books.route("/books/wip")
def wip():
    books = [b for b in get_filtered_books(request) if b['Status'] == 'WIP']
    return render_template("books.html", books=books)


@books.route("/books/read")
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
        out += "\n".join(f"- **{book['Title']}** by *{book['Author']}* ({book['Genre']})"
                for book in sorted(books, key=lambda x: x['Title']))
        out += "<br>"
    print(out)
    formatted = markdown(dedent(out))
    return render_template("raw.html", content=formatted, title="Books read")


@books.route("/books/")
def filter():
    filtered = get_filtered_books(request)
    categories = sorted(set([c['Genre'] for c in filtered]))
    out = []
    for category in categories:
        books_for_cat = [b for b in filtered if b['Genre'] == category]
        sorted_by_title = sorted(books_for_cat, key=lambda x: x['Title'])
        out.extend(sorted_by_title)
    return render_template("books.html", books=out)


@books.route("/books/new", methods=['POST'])
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
    return render_template("books.html", books=books[-10:], extra_pre=f"Added: {request.form['title']} by {request.form['author']}")


@books.route("/books/add")
def add():
    return render_template("add_book.html", title="Add a book")
