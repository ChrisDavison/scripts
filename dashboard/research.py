"""Routes for research questions"""
import json
import os

from flask import render_template, request, Blueprint

BP_RESEARCH = Blueprint("research", __name__, template_folder="templates")
RESEARCH_FILE = os.path.join(os.environ["DATADIR"], "research-summaries.json")


class Research:
    """Research represents a bunch of UoS research projects"""

    def __init__(self, filename):
        """Load in JSON research topics"""
        self.filename = filename
        self.data = json.load(open(os.path.expanduser(self.filename), "r"))

    def write(self):
        """Write data to file"""
        if self.data:
            json.dump(self.data, open(self.filename, "w"), indent=2)
        else:
            print("NO DATA")

    def append(self, item):
        """Append a new item to the internal data"""
        self.data.append(item)


@BP_RESEARCH.route("/research/")
def research():
    """Display all research projects"""
    projects = Research(RESEARCH_FILE)
    return render_template("research.html", research=projects.data)


@BP_RESEARCH.route("/research/new", methods=["POST"])
def new():
    """Write a new element to the file, from /research/add's form input"""
    projects = Research(RESEARCH_FILE)
    coauthors = [s.strip() for s in request.form["coauthor"].split(",")]
    projects.append(
        {
            "Topic": request.form["topic"],
            "Date": request.form["date"],
            "Author": request.form["leadauthor"],
            "Co-authors": coauthors,
            "Outline": [
                request.form["bullet-1"],
                request.form["bullet-2"],
                request.form["bullet-3"],
                request.form["bullet-4"],
                request.form["bullet-5"],
            ],
        }
    )
    Research.write()
    return render_template(
        "research.html",
        research=projects.data[-1:],
        extra_pre=f"Added: {request.form['topic']} by {request.form['leadauthor']}",
    )


@BP_RESEARCH.route("/research/add")
def add():
    """Present a form to add a new research project"""
    return render_template("add_research.html", title="Add research")
