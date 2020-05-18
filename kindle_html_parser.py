"""Parse highlights from a kindle"""
import sys
from bs4 import BeautifulSoup


data = open(sys.argv[1], 'r').read()
soup = BeautifulSoup(data, 'html.parser')
notes_and_highlights = soup.find_all(id=['highlight', 'note'])
h3 = soup.find('h3').text
fname = h3.replace(' ', '-') + '.org'
with open(fname.lower(), 'w') as f:
    print('#+TITLE:', h3 + ' notes', file=f)
    print('', file=f)
    print('*', h3, file=f)
    print('', file=f)

    for i, n in enumerate(notes_and_highlights):
        tidied = n.text.replace('\n', ' ')
        print('** highlight {}'.format(i), file=f)
        if n['id'] == 'note' and tidied:
            print('NOTE: ', end=' ', file=f)
        print(tidied, file=f)
        print('', file=f)
