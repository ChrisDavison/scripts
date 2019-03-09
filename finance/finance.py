import os
import pandas as pd
import sys
from textwrap import dedent

from flask import Flask, render_template, render_template_string, request
from jinja2 import Template
from markdown import markdown

app = Flask(__name__)

fn = os.environ['FINANCEFILE']

@app.route("/help")
def help():
    content = markdown(dedent("""
        # Help

        - `/` - view finances (with optional query params)
            - `y=YYYY` e.g. [`/?y=2019`](/?y=2019)
            - `m=MM` e.g. [`/?m=01`](/?m=01)
            - `q=QUERY` e.g. [`/?q=twitch`](/?q=twitch)
            - `cat=<CATEGORY>` (case-insensitive) e.g. [`/?cat=service`](/?cat=service)
            - Can be combined: [`/?y=2019&cat=Service`](/?y=2019&cat=Service)
        - `/help` - this view
        - `/new` - use a html form to add another finance entry, and write to file
    """))
    return render_template("raw.html", content=content)

@app.route("/")
def filter():
    finances = pd.read_csv(fn).sort_values(by='date')
    finances['year'] = finances['date'].apply(lambda x: str(x)[:4])
    finances['month'] = finances['date'].apply(lambda x: str(x)[5:7])
    yy=request.args.get('y')
    mm=request.args.get('m')
    cat=request.args.get('cat')
    query=request.args.get('q')
    finances = finances
    if cat:
        cat_low = cat.lower()
        filter_cat_low = finances.category.apply(lambda x: x.lower())
        finances = finances[filter_cat_low == cat_low]
    if yy:
        finances = finances[finances.year == yy]
    if mm:
        finances = finances[finances.month == mm]
    if query:
        lowdesc = finances.description.apply(lambda x: x.lower())
        finances = finances[lowdesc.str.contains(query.lower())]

    grouped = finances.groupby('category').agg('sum').sort_values(by='cost', ascending=False)
    output = """
    <br>{}<br>{}
    """.format(finances.set_index('date').to_html(), grouped.to_html())

    total = markdown(f"**Total: £{grouped.cost.sum():.0f}**")
    return render_template("index.html", finances=finances, extra_pre=total)

@app.route("/add", methods=['POST'])
def add():
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

@app.route("/new")
def new():
    return render_template("add.html")
