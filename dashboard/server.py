"""## Dashboard

- [`/finance/`](/finance/) **or** [and add a new entry](/finance/add)
- [`/books`](/books/) **or** [and add a new entry](/books/add)
- [`/research`](/research/) **or** [and add a new entry](/research/add)
- `/help` - this view
"""
import json
import os
from textwrap import dedent

from flask import Flask, render_template
from markdown import markdown

import finance
import books
import research

APP = Flask(__name__)
APP.register_blueprint(books.BP_BOOKS)
APP.register_blueprint(finance.BP_FINANCE)
APP.register_blueprint(research.BP_RESEARCH)


@APP.route("/")
@APP.route("/h")
@APP.route("/help")
def help():
    """Display help screen"""
    content = markdown(dedent(__doc__))
    return render_template("raw.html", content=content, title="Help")
