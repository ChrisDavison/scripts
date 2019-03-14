"""Routes for my reading list"""
import json
import os
from flask import request, render_template, Blueprint

BP_BOOKS = Blueprint("books", __name__, template_folder="templates")
BOOKS_FILE = os.path.join(os.environ["DATADIR"], "reading-list.json")


class Books:
    """Books represents a list of books"""

    def __init__(self, filename):
        """Load in the JSON file"""
        self.filename = filename
        self.data = []
        for b in json.load(open(BOOKS_FILE)):
            b["Read"] = "" if not b["Read"] else b["Read"]
            b["Author"] = "" if not b["Author"] else b["Author"]
            self.data.append(b)

    def write(self):
        """If data exists, write it to file"""
        if self.data:
            json.dump(self.data, open(self.filename, "w"), indent=2)
        else:
            print("NO DATA")

    def append(self, item):
        """Append an item to the internal data"""
        self.data.append(item)


@BP_BOOKS.route("/books/")
def book_list():
    """Render a list of books, with live filtering"""
    books_list = Books(BOOKS_FILE).data
    categories = sorted(set([c["Genre"] for c in books_list]))
    out = []
    for category in categories:
        books_for_cat = [b for b in books_list if b["Genre"] == category]
        sorted_by_title = sorted(books_for_cat, key=lambda x: x["Title"])
        out.extend(sorted_by_title)
    return render_template("books.html", books=out)


@BP_BOOKS.route("/books/new", methods=["POST"])
def new():
    """Add a new book, from the /books/add/ endpoint, to the file"""
    books = Books(BOOKS_FILE)
    books.append(
        {
            "Title": request.form["title"],
            "Author": request.form["author"],
            "Genre": request.form["genre"],
            "Status": request.form["status"],
            "Read": request.form["read"],
        }
    )
    books.write()
    return render_template(
        "books.html",
        books=books.data[-10:],
        extra_pre=f"Added: {request.form['title']} by {request.form['author']}",
    )


@BP_BOOKS.route("/books/add")
def add():
    return render_template("add_book.html", title="Add a book")
