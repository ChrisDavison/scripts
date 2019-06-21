#!/usr/bin/env python
"""Todo management."""
import datetime
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import click


VERSION = "0.1.0"
FILENAME_TODO = os.environ["TODOFILE"]
FILENAME_DONE = os.environ["DONEFILE"]
RE_DATE = re.compile(r"20\d\d-[0-1][0-9]-[0-2][0-9]")


@dataclass
class Todo:
    task: str
    scheduled: str
    finished: str

    def __str__(self):
        s = self.scheduled if self.scheduled else ""
        d = self.finished + " " if self.finished else ""
        return f"{d}{s:10s} {self.task}"

    def __contains__(self, query):
        return query.lower() in self.task.lower()

    @staticmethod
    def new(line):
        line = line.strip()
        if line.startswith("- "):
            line = line[2:]
        date, task = None, line
        if RE_DATE.match(line):
            date, task = line[:10], line[11:]
        return Todo(task, date, None)


@click.group()
def cli():
    """Manage todos in plaintext files.

    Filenames are recorded in $TODOFILE and $DONEFILE.
    Inspired by todo.txt/todo.sh, but with a much more streamlined approach.
    """
    pass


@cli.command(short_help="Add a todo")
@click.argument("text", nargs=-1)
def add(text):
    """Add a todo to $TODOFILE."""
    todo = Todo.new(" ".join(text))
    todos = parse_file(FILENAME_TODO)
    todos.append(todo)
    print(f"Added: {len(todos)-1}. {str(todo).lstrip()}")
    save_todos(todos, FILENAME_TODO)


@cli.command(short_help="Remove a todo")
@click.argument("idx", type=int)
def rm(idx):
    """Delete a todo."""
    todos = parse_file(FILENAME_TODO)
    todo = todos[idx]
    print(f"Remove: {len(todos)-1}. {str(todo).lstrip()}")
    del todos[idx]
    save_todos(todos, FILENAME_TODO)


@cli.command(short_help="Do todos")
@click.argument("IDX", nargs=-1)
def do(idx):
    """Move todos from $TODOFILE to $DONEFILE."""
    todos = parse_file(FILENAME_TODO)
    dones = parse_file(FILENAME_DONE)
    indexes = sorted([int(i) for i in idx])[::-1]
    valid_indexes = [i for i in indexes if i < len(todos)]
    for i in valid_indexes:
        todos[i].finished = datetime.date.today().strftime("%Y-%m-%d")
        dones.append(todos[i])
        del todos[i]
    save_todos(todos, FILENAME_TODO)
    save_todos(dones, FILENAME_DONE)


@cli.command(short_help="Undo todos")
@click.argument("IDX", nargs=-1)
def undo(idx):
    """Move todos from $DONEFILE into $TODOFILE"""
    todos = parse_file(FILENAME_TODO)
    dones = parse_file(FILENAME_DONE)
    indexes = sorted([int(i) for i in idx])[::-1]
    valid_indexes = [i for i in indexes if i < len(dones)]
    for i in valid_indexes:
        todos.append(dones[i])
        del dones[i]
    save_todos(todos, FILENAME_TODO)
    save_todos(dones, FILENAME_DONE)


@cli.command(short_help="Append text to end of todo")
@click.argument("idx", type=int)
@click.argument("text", nargs=-1)
def app(idx, text):
    todos = parse_file(FILENAME_TODO)
    todos[idx].task += " ".join(text)
    print(f"APPEND: {' '.join(text)}")
    save_todos(todos, FILENAME_TODO)


@cli.command(short_help="Prepend text to start of todo")
@click.argument("idx", type=int)
@click.argument("text", nargs=-1)
def prepend(idx, text):
    todos = parse_file(FILENAME_TODO)
    todos[idx].task = " ".join(text) + todos[idx].task
    print(f"PREPEND: {' '.join(text)}")
    save_todos(todos, FILENAME_TODO)


@cli.command(short_help="Schedule a task")
@click.argument("idx", type=int)
@click.argument("text", nargs=1)
def schedule(idx, text):
    """Schedule tasks with given date."""
    todos = parse_file(FILENAME_TODO)
    indexes = [int(i) for i in idx]
    for index in indexes:
        if RE_DATE.match(text):
            todos[index].scheduled = text
            print(f"SCHEDULE: {todos[index]}")
            save_todos(todos, FILENAME_TODO)


@cli.command(short_help="Unschedule a task")
@click.argument("idx", type=int)
def unschedule(idx):
    """Remove due date for tasks"""
    indexes = [int(i) for i in idx]
    for index in indexes:
        todos = parse_file(FILENAME_TODO)
        todos[index].scheduled = None
        print(f"UNSCHEDULE: {todos[index]}")
    save_todos(todos, FILENAME_TODO)


@cli.command(short_help="Schedule a command today")
@click.argument("idx", nargs=-1)
def today(idx):
    """Schedule tasks for today"""
    now = datetime.date.today().strftime("%Y-%m-%d")
    todos = parse_file(FILENAME_TODO)
    indexes = [int(i) for i in idx]
    for index in indexes:
        todos[index].task = f"{now} {todos[index]}"
        print(f"TODAY: {todos[index].task}")
    save_todos(todos, FILENAME_TODO)


@cli.command(short_help="List current todos")
@click.argument("query", default="")
def ls(query):
    """Print current tasks."""
    todos = parse_file(FILENAME_TODO)
    print_enumerated_todos(todos, filter=lambda _, x: query in x)


@cli.command(short_help="List done todos")
@click.argument("query", default="")
def lsd(query):
    """Print done tasks.  Optionally filtered."""
    dones = parse_file(FILENAME_DONE)
    print_enumerated_todos(dones, filter=lambda _, x: query in x)


@cli.command(short_help="List overdue tasks or tasks due today")
@click.argument("query", default="")
def due(query):
    """Print tasks due today, or overdue.  Optionally filtered."""
    todos = parse_file(FILENAME_TODO)
    print_enumerated_todos(todos, filter=lambda _, x: x.scheduled and query in x)


@cli.command(short_help="Print version")
def version():
    """Display current software version"""
    print(Path(__file__).stem, VERSION)


def parse_file(filename):
    """Get all todos in todofile"""
    return [Todo.new(line) for line in open(filename, "r")]


def print_enumerated_todos(todos, filter=lambda _: True):
    for i, task in enumerate(todos):
        if filter(i, task):
            print(f"{i:3d}. {task}")


def save_todos(todos, filename):
    with open(filename, "w") as f:
        for todo in todos:
            print("-", re.sub("\s\s+", " ", str(todo)), file=f)


if __name__ == "__main__":
    cli()
