#!/usr/bin/env python3
from pathlib import Path
from argparse import ArgumentParser

def is_header(line):
    first_word = line.split(' ')[0]
    return first_word == '#' * len(first_word)


def summarise_note(filepath):
    data = filepath.read_text()
    filesize = len(data)
    headers = [l for l in data.splitlines() if is_header(l)]
    n_header = len(headers)
    return (n_header, filesize, filepath)


def main(sort_by_headercount, show_top_n, words_to_ignore):
    notes = Path(".").expanduser().rglob("*.md")
    summarised_notes = [summarise_note(n) for n in notes
            if not any(word in str(n) for word in words_to_ignore)]
    if sort_by_headercount:
        summarised_notes.sort(key=lambda x: x[0], reverse=True)
    else:
        summarised_notes.sort(key=lambda x: x[1], reverse=True)
    header = "{:>10} {:>10} {}".format("#Headers", "#Bytes", "Filename")
    print(header)
    print("-" * len(header))
    for n_header, filesize, notename in summarised_notes[:show_top_n]:
        print("{:10} {:10} {}".format(n_header, filesize, notename))


if __name__ == "__main__":
    parser = ArgumentParser("large_notes")
    parser.add_argument("-m", action="store_true", default=False, 
            help="Sort by markdown header count, instead of filesize")
    parser.add_argument("-n", type=int, default=10, help="Show top N results")
    parser.add_argument("words_to_ignore", nargs="+", help="Words to ignore")
    args = parser.parse_args()
    main(args.m, args.n, args.words_to_ignore)

    
