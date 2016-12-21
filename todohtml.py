#!/usr/bin/env python
__border = """border-bottom: 1px dashed black"""
__fmt = """
<div style='display: flex; {border}'>
<div style='width: 5%; padding-top: 1em'>{p}</div>
<div style='width: 94%'>{ps}</div>
</div>
"""

def filter_priority(p, ls):
    match = ['- {}'.format(r[7:]) for r in ls 
            if r.startswith("-   {}".format(p))
            and '#personal' not in r]
    return ''.join(match)
    

if __name__ == "__main__":
    fn="/Users/davison/Dropbox/notes/todo.md"
    todos = [row for row in open(fn) if row.startswith('-')]
    out = ""
    for priority in ['A', 'B', 'C', 'D', 'Z']:
        prio = filter_priority(priority, todos)
        border = __border if priority != 'Z' else ''
        out += __fmt.format(p=priority, ps=prio, border=border)
    print(out)

