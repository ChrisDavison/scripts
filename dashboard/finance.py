"""## Finances

- [`/finance/` (with optional query params)](/finance/)
    - [`y=YYYY` e.g. 2019](/finance/?y=2019)
    - [`m=MM` e.g. January](/finance/?m=01)
    - [`q=QUERY` e.g. twitch](/finance/?q=twitch)
    - [`cat=<CATEGORY>`, e.g. find services](/finance/?cat=service)
    - `json=1` - return the json representation of the main table
- [`/finance/categories`](/finance/categories) - links to each unique category
- [`/finance/unique` purchases](/finance/unique) - links to each unique purchase
- [`/finance/add` entry ](/finance/add)
"""
import json
import os
import pandas as pd
import sys
from textwrap import dedent

from flask import Flask, render_template, request, Blueprint
from markdown import markdown

app = Flask(__name__)

fn = os.environ['FINANCEFILE']
finance = Blueprint('finance', __name__, template_folder='templates')


@finance.route("/finance/help")
def financehelp():
    content = markdown(dedent(__doc__))
    return render_template("raw.html", content=content, title="Help")


@finance.route("/finance/categories")
def categories():
    categories = pd.read_csv(fn).sort_values(by='category')['category'] \
        .unique().tolist()
    no_space = lambda x: x.replace(' ', '%20')
    categories_as_list = "\n".join([f"- [{c}](/finance/?cat={no_space(c)})" for c in categories])
    formatted = markdown(dedent(categories_as_list))
    return render_template("raw.html", content=formatted, title="categories")


@finance.route("/finance/uniques")
def uniques():
    uniques = pd.read_csv(fn).sort_values(by='description')['description'] \
        .unique().tolist()
    no_space = lambda x: x.replace(' ', '%20')
    uniques_as_list = "\n".join([f"- [{c}](/finance/?q={no_space(c)})" for c in uniques])
    formatted = markdown(dedent(uniques_as_list))
    return render_template("raw.html", content=formatted, title="Unique Purchases")


@finance.route("/finance/")
def filter():
    finances = pd.read_csv(fn).sort_values(by='date')
    finances['year'] = finances['date'].apply(lambda x: str(x)[:4])
    finances['month'] = finances['date'].apply(lambda x: str(x)[5:7])
    yy=request.args.get('y')
    mm=request.args.get('m')
    cat=request.args.get('cat')
    query=request.args.get('q')
    if cat:
        cat_low = cat.lower()
        filter_cat_low = finances.category.apply(lambda x: x.lower())
        finances = finances[filter_cat_low.str.startswith(cat_low)]
    if yy:
        finances = finances[finances.year == yy]
    if mm:
        finances = finances[finances.month == mm]
    if query:
        lowdesc = finances.description.apply(lambda x: x.lower())
        finances = finances[lowdesc.str.contains(query.lower())]
    total = markdown(f"**Total: £{finances.cost.sum():.0f}**")
    if request.args.get('json'):
        ord=['date', 'cost', 'category', 'description']
        js = finances[ord].to_json(orient='records')
        return json.dumps(json.loads(js), indent=2)
    return render_template("finances.html", finances=finances, extra_pre=total)


@finance.route("/finance/new", methods=['POST'])
def new():
    finances = pd.read_csv(fn).sort_values(by='date')
    finances = finances.financeend({
        'date': request.form['date'],
        'description': request.form['description'],
        'category': request.form['category'],
        'cost': float(request.form['cost'])
    }, ignore_index=True)
    finances[['date', 'cost', 'category', 'description']].to_csv(os.environ['FINANCEFILE'], index=False)
    return render_template("finances.html", 
            finances=finances.iloc[finances.index.size - 10:],
            extra_pre="<strong>Last 10</strong>")


@finance.route("/finance/add")
def add():
    return render_template("add_expense.html", title="Add a new purchase")
