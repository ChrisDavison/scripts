import sys
from bs4 import BeautifulSoup

data = open(sys.argv[1], 'r').read()
soup = BeautifulSoup(data, 'html.parser')

notes_and_highlights = [h for h in soup.find_all(id=['highlight', 'note'])]

def tidy(note):
    return note.text.replace('\n', ' ')

h3 = soup.find('h3').text
fname = h3.replace(' ', '-') + '.txt'
with open(fname.lower(), 'w') as f:
    print('#', h3, file=f)
    print('', file=f)


    for n in notes_and_highlights:
        tidied = tidy(n)
        if n['id'] == 'note' and tidied:
            print('NOTE: ', end=' ', file=f)
        print(tidy(n), file=f)
        print('', file=f)
        
