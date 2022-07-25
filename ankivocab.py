#!/usr/bin/env python
"""Anki Vocab Helper

Usage: ankivocab <word> [<language>]
"""
from docopt import docopt
import subprocess
from time import sleep


def run_searches(word, language=""):
    """Run google search for the word, sentence, and an image."""
    # If language is provided, run a definition and sentence search for the language
    word = word.replace(' ', '%20')
    language = language.lower()
    if language in ['korean', 'hangul', 'ko', 'kr']:
        urls = [
            f"https://www.google.com/search?hl=en&q={word}%20definition",
            f"https://www.google.com/search?hl=en&q={word}%20sentence",
            f"https://www.google.com/search?tbm=isch&q={word}&tbs=imgo:1",
            "https://korean.dict.naver.com/koendict/#/search?query={word}"
            f"https://en.dict.naver.com/#/search?query={word}"
        ]

        subprocess.run(["firefox", "--new-window", urls[0]], check=True)
        sleep(0.2)
        for u in urls[1:]:
            subprocess.run(["firefox", "--new-tab", u], check=True)
            sleep(0.1)
    else:
        print("Not set up language", language, "yet")
    # elif language:
    #     google_definition += f"%20{language}"
    #     google_sentence += f"%20{language}"
    #     subprocess.run(["firefox", google_definition], check=True)
    #     subprocess.run(["firefox", google_sentence], check=True)


if __name__ == "__main__":
    ARGS = docopt(__doc__)
    run_searches(ARGS["<word>"], ARGS.get("<language>", ""))
