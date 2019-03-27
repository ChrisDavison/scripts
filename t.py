#!/usr/bin/env python3
import os
import re


def parse_todo(line):
    line = line.strip()
    if line.startswith("- "):
        line = line[2:]
    date, task = None, line
    if re.match("\d\d\d\d-\d\d-\d\d", line):
        date, task = line[:10], line[11:]
    return {"task": task, "date": date, "done": False}


def printable(task):
    d = task["date"] if task["date"] else ""
    return f"{task['idx']:3d}. {d:10s} {task['task']}"


def writeable(task):
    d = task["date"] if task["date"] else ""
    return f"- {task['idx']:3d}. {d:10s} {task['task']}"


def parse_file(filename, parser):
    return [{**parser(line), "idx": i} for i, line in enumerate(open(filename, "r"))]


for line in parse_file(os.environ["TODOFILE"], parse_todo):
    print(printable(line))
