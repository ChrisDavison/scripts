#!/usr/bin/env python3
import os
import argparse
import re

# Regex
# Instead, a list of keywords, which I prepend onto the regex
# and then search with this?
rEntr = re.compile('@([a-zA-Z0-9]+)[{]')
rKeyw = re.compile('@.*?[{](.*?),')
regex = re.compile('(author|journal|title|year|url) = ([{].*?[}][,} ])')

menu = """Bibliography Tool
=================
1) Search for an entry
2) Add an entry
3) List a certain detail
4) Add via DOI number
"""

class bibliography:
    fn = ""
    entries = {}
    def __init__(self, fn):
        self.fn = fn
        self.parse_file(fn)

    def parse_file(self, filename):
        lines = [line for line in open(filename)]
        lines = lines[5:]

        for line in lines:
            try:
                k, v = self.parse_entry(line)
            except:
                continue
            self.entries[k] = v

    def parse_entry(self, line):
        try:
            type = re.match(rEntr, line).groups()[0]
            keyword = re.match(rKeyw, line).groups()[0]

            matches = re.findall(regex, line) 
            out = [match for match in matches]
            out.append(('type', type))

            return keyword, out
        except:
            return 

    def search(keyword):
        pass

    def add():
        pass

    def delete():
        pass

    def edit():
        pass

def main():
    mybib = bibliography("library.bib")
    for keyword, details in mybib.entries.items():
        print(keyword)
        for detail in details:
            key, value = detail
            print("{:>15} - {}".format(key, value))
        print("-"*80)
        print("-"*80)

if __name__ == "__main__":
    main()
