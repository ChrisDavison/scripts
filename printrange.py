#!/usr/bin/env python3
import argparse
import sys


def print_lines(*, filename=None, start=None, end=None, compare_with=None):
    """Print lines, optionally with start and end date.

    By default the printer is "dumb"...it will print if _start_ or _end_ text is in the line.
    With the compare_with option set >= 0, it'll do comparison with that specific column (using
    comma as column delimiter).

    Arguments
    ---------
    filename : str (default: None)
        Filename of the file to filter
    start : str (default: None)
        If this string is in the line, start printing lines.  None => print immediately
    end : str (default: None)
        If this string is in the line, quit.  None => print till EOF
    compare_with : int (default: None)
        Column to use for compare_with.  None => just check for presence of string, not >= or <=.
    """
    assert compare_with is None or compare_with >= 0, "compare_with must be None or >=0"

    def should_print(line):
        """Closure to simplify comparison for starting printing."""
        if compare_with is not None:
            return start >= line.split(" ")[compare_with]
        else:
            return start in line

    def should_quit(line):
        """Closure to simplify comparison for stopping printing."""
        if compare_with is not None:
            return end >= line.split(" ")[compare_with]
        else:
            return end in line

    with open(filename, "r") as file_in:
        printing = not start
        for line in file_in:
            if not printing and should_print(line):
                printing = True
            if printing:
                print(line.strip())
            if should_quit(line):
                break
    return 0


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser("printrange")
    PARSER.add_argument("filename")
    PARSER.add_argument("--after", type=str)
    PARSER.add_argument("--before", type=str)
    PARSER.add_argument("--compare-with", type=int)
    ARGS = PARSER.parse_args()
    print(ARGS)
    sys.exit(
        print_lines(
            filename=ARGS.filename,
            start=ARGS.after,
            end=ARGS.before,
            compare_with=ARGS.compare_with,
        )
    )
