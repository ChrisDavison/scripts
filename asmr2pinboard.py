#!/usr/bin/env python3
import os
import sys

html = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks Menu</H1>

<DL><p>
{bookmarks}
</DL>"""


def to_pinboard(string):
    title, id = string.strip().split(";")
    if title.startswith("+"):
        title = title[1:]
    link = "https://www.youtube.com/watch?v={}".format(id)
    return '<DT><A HREF="{link}">{title}</A>'.format(link=link, title=title)


def main():
    filename = os.environ["ASMRFILE"]
    entries = open(filename).read().split("\n")
    formatted_entries = "\n".join(to_pinboard(e) for e in entries if e)
    print(html.format(bookmarks=formatted_entries))


if __name__ == "__main__":
    main()
