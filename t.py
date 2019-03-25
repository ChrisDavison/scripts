#!/usr/bin/env python3
import os
import re
from dataclasses import dataclass
from typing import Optional, List, Any

@dataclass
class Todo:
    due: Optional[str]
    task: str

    def __repr__(self):
        d = self.due if self.due else ''
        return f"{d:10s} {self.task}"


def parse_todo(line: str) -> Todo:
    line = line.strip()
    if line.startswith("- "):
        line = line[2:]
    date, task = None, line
    if re.match("\d\d\d\d-\d\d-\d\d", line):
        date, task = line[:10], line[11:]
    return Todo(date, task)


def add(text: str) -> Todo:
    m = re.match(r"(\d{4}-\d{2}-\d{2}) (.*)", text)
    due, task = (m.group(1), m.group(2)) if m else (None, text)
    t = Todo(due, task)
    return t

todos = [parse_todo(line) for line in open(os.environ["TODOFILE"], 'r')]
text = "2019-01-01 This is a task"
todos.append(add(text))

for t in todos:
    print(t)
