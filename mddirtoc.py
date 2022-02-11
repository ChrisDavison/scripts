#!/usr/bin/env python3
import sys
from pathlib import Path
import re

def main(direc):
    files = Path(direc).glob('*.md')
    re_header = re.compile("^(#+) (.*)")
    out = []
    for f in files:
        headers = []
        for line in f.read_text().splitlines():
            if m := re_header.search(line):
                headers.append((len(m.group(1))-1, m.group(2)))
        linkpath = f.relative_to(".")
        headers[0] = (headers[0][0], f"[{headers[0][1]}](./{linkpath})")
        out.extend(headers)
    outstr = f"# Table of Contents - {direc}\n\n"
    for indent, line in out:
        pad = "    " * indent
        outstr += pad + "- " + line + "\n"
    print(outstr)


if __name__ == "__main__":
    args = sys.argv[1:]
    direc = args[0] if len(args) > 0 else "."
    main(direc)
