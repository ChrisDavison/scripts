"""Routes for my purchase history"""
import json
import os

from flask import render_template, Blueprint
from markdown import markdown

BP_FINANCE = Blueprint("finance", __name__, template_folder="templates")
PURCHASE_FILE = os.path.join(os.environ["DATADIR"], "finances.json")


class Purchases:
    """Purchases represents a json file of expenditures"""

    def __init__(self, filename):
        """Initialise a purchase list, loading in a file"""
        self.filename = filename
        self.data = list(
            sorted(json.load(open(self.filename)), key=lambda x: x["date"])
        )

    def write(self):
        """If we have data, write it to file"""
        if self.data:
            json.dump(self.data, open(self.filename, "w"), indent=2)
        else:
            print("NO DATA")

    def append(self, item):
        """Add an item to the internal data"""
        self.data.append(item)


@BP_FINANCE.route("/finance/")
def finances():
    """Return all purchases"""
    purchases = Purchases(PURCHASE_FILE).data
    total = sum([f["cost"] for f in purchases])
    categories = ", ".join(set(f["category"] for f in purchases))
    total_str = markdown(f"**Total: £{total:.0f}**\nCategories: {categories}")
    return render_template("finances.html", finances=purchases, extra_pre=total_str)


@BP_FINANCE.route("/finance/new", methods=["POST"])
def new():
    """Create a new finance purchase, and write to json"""
    purchases = Purchases(PURCHASE_FILE)
    purchases.append(
        {
            "date": request.form["date"],
            "description": request.form["description"],
            "category": request.form["category"],
            "cost": float(request.form["cost"]),
        }
    )
    purchases.write()
    return render_template(
        "finances.html",
        finances=finances.data[-10:],
        extra_pre="<strong>Last 10</strong>",
    )


@BP_FINANCE.route("/finance/add")
def add():
    """Form to add a new expense/purchase"""
    return render_template("add_expense.html", title="Add a new purchase")
