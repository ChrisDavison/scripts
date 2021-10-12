#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys


def get_capture_options():
    capturedir = Path("~/code/scripts/capture").expanduser()
    capture_scripts = dict()
    for script in capturedir.rglob('*.py'):
        desc = ""
        for line in script.open():
            line = line.strip()
            if line.startswith('"""'):
                desc = line.replace('"', '')
                break
        capture_scripts[script.stem] = {
                'filename': script,
                'description': desc
        }
    return capture_scripts


def print_capture_options():
    options = get_capture_options()
    for name in options:
        print(f"{name}\n    {options[name]['description']}")


def run_capture(choice):
    options = get_capture_options()
    chosen = options.get(choice, None)
    if not chosen:
        print("'{choice}' not in options")
        print("Options: {list(options.keys())}")
        return
    print(f"{choice}\n    {chosen['description']}\n")
    subprocess.run(str(chosen['filename']),
                   stdin=sys.stdin, stdout=sys.stdout,
                   check=True)


if len(sys.argv) > 1:
    run_capture(sys.argv[1])
else:
    print_capture_options()    
