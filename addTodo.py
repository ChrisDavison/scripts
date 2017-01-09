#! /usr/bin/env python

fn = '/Users/davison/Dropbox/notes/todo.md'

todos = set(line for line in open(fn) if line.startswith('-'))
personal = set(line for line in todos if '#personal' in line)
work = todos - personal

for todo in sorted(work):
    print todo.strip('\n')
