"""## Research

Research currently going on at UoS.

- - [`/research/help`](/research/help) for this view
"""
import json
import os
from collections import defaultdict
from textwrap import dedent

import dateutil
from flask import render_template, request, Blueprint
from markdown import markdown

bp_research = Blueprint('research', __name__, template_folder='templates')


@bp_research.route("/research/help")
def researchhelp():
    content = markdown(dedent(__doc__))
    return render_template("raw.html", content=content, title="Help")


# @books.route("/books/genres")
# def genres():
#     genres = sorted(set(b['Genre'] for b in get_books()))
#     no_space = lambda x: x.replace(' ', '%20')
#     genres_as_list = "\n".join([f"- [{c}](/books/?genre={no_space(c)})" for c in genres])
#     formatted = markdown(dedent(genres_as_list))
#     return render_template("raw.html", content=formatted, title="genres")


@bp_research.route("/research/")
def research():
    fn = "~/Dropbox/data/research-summaries.json"
    projects = json.load(open(os.path.expanduser(fn), "r"))
    return render_template("research.html", research=projects)


# @books.route("/books/new", methods=['POST'])
# def new():
#     books = get_books()
#     books.append({
#         'Title': request.form['title'],
#         'Author': request.form['author'],
#         'Genre': request.form['genre'],
#         'Status': request.form['status'],
#         'Read': request.form['read']
#     })
#     json.dump(books, open(fn, 'w'), indent=2)
#     return render_template("books.html", books=books[-10:], extra_pre=f"Added: {request.form['title']} by {request.form['author']}")


# @books.route("/books/add")
# def add():
#     return render_template("add_book.html", title="Add a book")
