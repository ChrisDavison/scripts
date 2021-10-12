#!/usr/bin/env python3
"Quickly capture something to todays journal."""
import textwrap
from pathlib import Path
from datetime import date, datetime


def capture():
    """Capture a note and save to todays journal."""
    notedir = Path("~/code/knowledge/journal").expanduser()
    todays_journal = notedir / date.today().strftime("%Y-%m-%d-%A.md")
    timestamp = datetime.now().strftime("(%H:%M)")
    contents = todays_journal.read_text().splitlines()
    print("\nCapture note to today's journal")
    note = f"**{timestamp}** " + input("> ")
    first_h2 = [i for i, n in enumerate(contents) if n[:2] == '##']
    if first_h2:
        contents.insert(first_h2[0], f"{textwrap.fill(note, 80)}\n")
    else:
        contents.insert(1, f"\n{textwrap.fill(note, 80)}")
    todays_journal.write_text('\n'.join(contents))


if __name__ == "__main__":
    capture()
