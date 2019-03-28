#!/usr/bin/env python3
"""Todo management."""
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import click


VERSION = "0.1.0"
FILENAME_TODO = os.environ["TODOFILE"]
FILENAME_DONE = os.environ["DONEFILE"]


@dataclass
class Todo:
    task: str
    scheduled: str
    finished: str

    def __str__(self):
        s = self.scheduled if self.scheduled else ""
        return f"{s:10s} {self.task}"

    def __contains__(self, query):
        return query.lower() in self.task.lower()

    @staticmethod
    def new(line):
        line = line.strip()
        if line.startswith("- "):
            line = line[2:]
        date, task = None, line
        if re.match("\d\d\d\d-\d\d-\d\d", line):
            date, task = line[:10], line[11:]
        return Todo(task, date, None)


@click.group()
def cli():
    pass


@cli.command(short_help="Add a todo")
@click.argument("text")
def add(text):
    #     todo = Todo.new(' '.join(args['TEXT']))
    #     todos.append(todo)
    #     print(f"Added: {len(todos)}. {str(todo).lstrip()}")
    #     # save_todos(todos, FILENAME_TODO)
    pass

@cli.command(short_help = "Remove a todo")
@click.argument("IDX")
def rm(idx):
    #     idx = int(args['IDX'])
    #     todo = todos[idx]
    #     print(f"Remove: {len(todos)}. {str(todo).lstrip()}")
    #     del todos[idx]
    #     # save_todos(todos, FILENAME_TODO)
    #     pass
    pass

@cli.command(short_help="Do todos")
@click.argument("IDX...")
def do(text):
    pass

@cli.command(short_help="Undo todos")
@click.argument("IDX", nargs=-1)
def undo(idx):
    pass

@cli.command(short_help="Append text to end of todo")
@click.argument("idx")
@click.argument("text", nargs=-1)
def app(idx, text):
    print(idx)
    print(" ".join(text))
    #     idx = int(args['IDX'])
    #     todos[idx].task += ' '.join(args["TEXT"])
    #     save_todos(todos, FILENAME_TODO)
    pass

@cli.command()
@click.argument("text")
def prepend(text):
    #     idx = int(args['IDX'])
    #     todos[idx].task = ' '.join(args["TEXT"]) + " " + todos[idx].task
    #     save_todos(todos, FILENAME_TODO)
    pass

@cli.command()
@click.argument("text")
def schedule(text):
    pass

@cli.command()
@click.argument("text")
def unschedule(text):
    pass

@cli.command()
@click.argument("text")
def today(text):
    pass

@cli.command()
@click.argument("query", default="")
def ls(query):
    todos = parse_file(FILENAME_TODO)
    for i, todo in enumerate(todos):
        if query in todo:
            print(f"{i:3d}. {todo}")

@cli.command()
@click.argument("text")
def lsd(text):
    pass

@cli.command()
@click.argument("text")
def due(text):
    pass


@cli.command()
def version():
    print(Path(__file__).stem, VERSION)


def parse_file(filename):
    todos = []
    for i, line in enumerate(open(filename, 'r')):
        todos.append(Todo.new(line))
    return todos


def save_todos(todos, filename):
    if 0:
        with open(filename, 'w') as f:
            for todo in todos:
                print(f"- {str(todo).lstrip()}", file=f)
    else:
        print("NOT SAVED. Still testing code")


if __name__ == "__main__":
    cli()
