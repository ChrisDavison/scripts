#!/usr/bin/env python3
from pathlib import Path
import pyperclip

here = Path('.')
new = input("Filename: ") + ".md"
desc = input("Link text: ")
newfn = here / new
if newfn.exists():
    raise Exception("File already exists")
newfn.write_text(pyperclip.paste())
out = f"[{desc}]({newfn.relative_to(here)})"
pyperclip.copy(out)
