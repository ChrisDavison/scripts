"""## Dashboard

- [`/finance/`](/finance/), and [help for routes under `/finance/`](/finance/help)
- [`/books`](/books/), and [help for routes under `/books/`](/books/help)
- `/help` - this view
"""
import json
import os
import pandas as pd
import sys
from textwrap import dedent

from flask import Flask, render_template, request
from markdown import markdown

import finance
import books

app = Flask(__name__)
app.register_blueprint(books.books)
app.register_blueprint(finance.finance)


@app.route("/")
@app.route("/h")
@app.route("/help")
def help():
    content = markdown(dedent(__doc__))
    return render_template("raw.html", content=content, title="Help")
