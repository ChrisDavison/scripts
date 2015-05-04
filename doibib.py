#!/usr/bin/env python3
import os
import argparse
import re

# Regex
# Instead, a list of keywords, which I prepend onto the regex
# and then search with this?
rEntr = re.compile('@(?P<entry_type>[a-zA-Z0-9]+){')
keywords = ["author", "journal", "title", "year"]
regexs =  {kw: "(?P<{}>{} = ({}) ".format(kw, kw, ".*?") for kw in keywords}

class bib_entry:
    entry_type = ""
    author = ""
    title = ""
    journal = ""
    url = ""

class bibliography:
    fn = ""
    contents = None
    def __init__(self, fn):
        # 
        self.fn = fn
        self.__parse(fn)

    def __parse(self, filename):
        lines = [line for line in open(filename)]
        lines = lines[5:]
        for line in lines:
            type = re.match(rEntr, line)
            if type:
                print(type.group('entry_type'))
            out = []
            for kw, regex in regexs.items():
                m = re.match(regex, line)
                if m:
                    print(m.group(kw))
            print(out)

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

if __name__ == "__main__":
    main()
