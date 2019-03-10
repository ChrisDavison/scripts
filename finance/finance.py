"""
## Views

- `/` - view finances (with optional query params)
    - `y=YYYY` e.g. [`/?y=2019`](/?y=2019)
    - `m=MM` e.g. [`/?m=01`](/?m=01)
    - `q=QUERY` e.g. [`/?q=twitch`](/?q=twitch)
    - `cat=<CATEGORY>` (case-insensitive) e.g. [`/?cat=service`](/?cat=service)
    - `json=1` - return the json representation of the main table
- [`/categories`](/categories) - links to each unique category
- [`/uniques`](/uniques) - links to each unique purchase
- `/help` - this view

## Modification

- [`/add`](/add) - Add a new purchase

---

Like usual, GET queries can be chained together with `&` (e.g. [2019 services](/?cat=service&y=2019))
"""
import json
import os
import pandas as pd
import sys
from textwrap import dedent

from flask import Flask, render_template, request
from markdown import markdown

app = Flask(__name__)

fn = os.environ['FINANCEFILE']

@app.route("/h")
@app.route("/help")
def help():
    content = markdown(dedent(__doc__))
    return render_template("raw.html", content=content, title="Help")

@app.route("/categories")
def categories():
    categories = pd.read_csv(fn).sort_values(by='category')['category'] \
        .unique().tolist()
    no_space = lambda x: x.replace(' ', '%20')
    categories_as_list = "\n".join([f"- [{c}](/?cat={no_space(c)})" for c in categories])
    formatted = markdown(dedent(categories_as_list))
    return render_template("raw.html", content=formatted, title="categories")

@app.route("/uniques")
def uniques():
    uniques = pd.read_csv(fn).sort_values(by='description')['description'] \
        .unique().tolist()
    no_space = lambda x: x.replace(' ', '%20')
    uniques_as_list = "\n".join([f"- [{c}](/?q={no_space(c)})" for c in uniques])
    formatted = markdown(dedent(uniques_as_list))
    return render_template("raw.html", content=formatted, title="Unique Purchases")

@app.route("/")
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
    total = markdown(f"**Total: £{grouped.cost.sum():.0f}**")
    if request.args.get('json'):
        ord=['date', 'cost', 'category', 'description']
        js = finances[ord].to_json(orient='records')
        return json.dumps(json.loads(js), indent=2)
    return render_template("index.html", finances=finances, extra_pre=total)

@app.route("/new", methods=['POST'])
def new():
    finances = pd.read_csv(fn).sort_values(by='date')
    finances = finances.append({
        'date': request.form['date'],
        'description': request.form['description'],
        'category': request.form['category'],
        'cost': float(request.form['cost'])
    }, ignore_index=True)
    finances[['date', 'cost', 'category', 'description']].to_csv(os.environ['FINANCEFILE'], index=False)
    return render_template("index.html", 
            finances=finances.iloc[finances.index.size - 10:],
            extra_pre="<strong>Last 10</strong>")

@app.route("/add")
def add():
    return render_template("add.html", title="Add a new purchase")
