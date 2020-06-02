#!/usr/bin/env python3
"""Reference for a website, in IEEE format"""
import dateutil.parser as dp
import pyperclip
import os

authors = []
while True:
    author = input("Author: ")
    if author == "":
        break
    authors.append(author)
title = input("Title: ")
url = input("URL: ")
publisher = input("Publisher: ")
year = input("Year of publication: ")
accessed = dp.parse(input("Date accessed: "))
doi = input("DOI: ")

authors = [a.title() for a in authors]
if len(authors) > 1:
    authors[-1] = 'and ' + authors[-1]

formatted_authors = ', '.join(authors)

msg = formatted_authors
msg += ", '{}'".format(title)
if year:
    msg += ", {}".format(year)
if publisher:
    msg += ", {}".format(publisher)
msg += ", {} Accessed: {}".format(url, accessed.strftime("%d %b %Y"))
if doi:
    msg += ", doi: {}".format(doi)

os.system('cls' if os.name == 'nt' else 'clear')
print("SAVED TO CLIPBOARD")
print(msg)
pyperclip.copy(msg)
