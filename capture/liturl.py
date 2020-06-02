#!/usr/bin/env python3
import dateutil.parser as dp
import pyperclip

authors = []
while True:
    author = input("Author: ")
    if author == "":
        break
    authors.append(author)
title = input("Title: ")
url = input("URL: ")
year = input("Year of publication: ")
accessed = dp.parse(input("Date accessed: "))

authors = [a.title() for a in authors]
if len(authors) > 1:
    authors[-1] = 'and ' + authors[-1]

formatted_authors = ', '.join(authors)

msg = """{formatted_authors}, '{title}', {year}, {url} Accessed: {access_date}""".format(formatted_authors=formatted_authors, title=title, year=year, url=url, access_date=accessed.strftime("%d %b %Y"))

print(msg)
pyperclip.copy(msg)
print('...saved to clipboard')
