"""
## Views

- `/` - view books (with optional query params)
    - `r=0|1` Books that have been read
    - `genre=<GENRE>`
    - `s=<STATUS>`
    - `query=<QUERY>` - Search in title and author
- [`/read`](/read)
- [`/genres`](/genres)
- `/help` - this view

## Modification

- [`/add`](/add) - Add a new purchase
"""
import json
import os
import pandas as pd
import sys
from textwrap import dedent

from flask import Flask, render_template, request
from markdown import markdown

app = Flask(__name__)

fn = "/Users/davison/Dropbox/data/reading-list.json"

def get_books():
    books = json.load(open(fn))
    tidied = []
    for b in books:
        b['Read'] = '' if not b['Read'] else b['Read']
        tidied.append(b)
    return tidied


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


@app.route("/read")
def read():
    books = sorted([b for b in get_books() if b['Read']], key=lambda x: x['Title'])
    books_as_list = "\n".join([f"- **{b['Title']}** by *{b['Author']}* ({b['Genre']}))" for b in books])
    formatted = markdown(dedent(books_as_list))
    return render_template("raw.html", content=formatted, title="genres")


@app.route("/")
def filter():
    books = get_books()
    genre=request.args.get('genre', '').lower()
    status=request.args.get('s', '').lower()
    read=request.args.get('r', '').lower()
    query=request.args.get('query', '').lower()
    if genre:
        books = [b for b in books if b['Genre'].lower().startswith(genre)]
    if read:
        books = [b for b in books if b['Read']]
    if status:
        books = [b for b in books if b['Status'].lower() == status]
    if query:
        books = [b for b in books if any(query in b['Author'], query in b['Title'])]
    return render_template("index.html", books=books)


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
