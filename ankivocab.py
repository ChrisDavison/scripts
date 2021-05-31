#!/usr/bin/env ipython
"""Anki Vocab Helper

Usage: ankivocab <word> [<language>]"""
from docopt import docopt
import subprocess


def run_searches(word, language=None):
    """Run google search for the word, sentence, and an image."""
    google_definition = f"https://www.google.com/search?hl=en&q={word}%20definition"
    google_sentence = f"https://www.google.com/search?hl=en&q={word}%20sentence"
    google_image = f"https://www.google.com/search?tbm=isch&q={word}&tbs=imgo:1"

    subprocess.run(["firefox", google_definition], check=True)
    subprocess.run(["firefox", google_sentence], check=True)
    subprocess.run(["firefox", google_image], check=True)

    # If language is provided, run a definition and sentence search for the language
    if language:
        google_definition += f"%20{language}"
        google_sentence += f"%20{language}"
        subprocess.run(["firefox", google_definition], check=True)
        subprocess.run(["firefox", google_sentence], check=True)


if __name__ == "__main__":
    ARGS = docopt(__doc__)
    run_searches(ARGS["<word>"], ARGS["<language>"])
