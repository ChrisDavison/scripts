#!/usr/bin/env python3
"""Capture a literature entry"""
import pyperclip
import requests
from doi2bib import crossref

title = input("Title: ")

authors = []
while True:
    author = input("Author: ")
    if author == "":
        break
    authors.append(author)
authors = [a.title() for a in authors]
if len(authors) > 1:
    authors[-1] = 'and ' + authors[-1]

joined_authors = ' and '.join(authors)

found, bibtex = crossref.get_bib(input("DOI: "))
filename = title.lower().replace(' ', '-') + ".pdf"

print('-'*40)
msg = "## {}\n".format(title)
msg += "\nAuthors: {}".format(joined_authors)
if not found:
    bibtex = ''
msg += "\n\n``` bibtex\n{}\n```".format(bibtex)
print(msg)
print('-'*40)
print('...copied entry to clipboard.')
print('Hit <Enter> to copy filename to clipboard')
pyperclip.copy(msg)
print('-'*40)
print('Filename:', filename)
input()
pyperclip.copy(filename)
print('...copied filename to clipboard')
