import re
import requests
import sys

rEntr = re.compile('@([a-zA-Z0-9]+)[{]')
rKeyw = re.compile('@.*?[{](.*?),')
regex = re.compile('(author|journal|title|year|url)\s?=\s?([{].*?[}][,} ])')


class bibentry:
    keyword = ""
    entrytype = ""
    details = {}
    def __init__(self, keyword, entrytype, details):
        self.entrytype = entrytype
        self.keyword = keyword
        self.details = details

    def __str__(self):
        out = "{:<18}<<{}>>\n".format(self.keyword, self.entrytype)
        for key, value in self.details:
            out += "{:>15} - {}\n".format(key, value)
        out += "-"*80
        return out

class bibliography:
    entries = {}  # Entries is a dict of KEYWORD:bibentry
    def __init__(self, fn):
        self.fn = fn
        try:
            self.parse_file(fn)
        except Exception as E:
            print("Failed parsing.")
            sys.exit(E)

    def parse_file(self, filename):
        lines = [line for line in open(filename)]
        lines = lines[5:] # Skip Mendeley's stuff...

        for line in lines:
            try:
                k, t, v = self.parse_entry(line)
            except:
                continue
            if k and t and v:
                self.entries[k] = bibentry(k, t, v)

    def parse_entry(self, line):
        try:
            entrytype = re.match(rEntr, line).groups()[0]
            keyword = re.match(rKeyw, line).groups()[0]

            matches = re.findall(regex, line) 
            out = [match for match in matches]

            return keyword, entrytype, out
        except:
            return 

    def search(self, searchword):
        for keyword, entry in self.entries.items():
            for detail in entry.details:
                key, value = detail
                if searchword in value:
                    print(entry)

    def add(self):
        print("Fix bibliography.add()")
        pass

    def delete(self):
        print("Fix bibliography.delete()")
        pass

    def edit(self):
        print("Fix bibliography.edit()")
        pass

    def __str__(self):
        out = [entry.__str__() for entry in self.entries.values()]
        return "\n".join(out)
       
    def from_doi(self, doi):
        accept='text/x-bibliography; style=bibtex'
        if not doi.startswith("http://"):
            doi = "http://dx.doi.org/" + doi
        r = requests.get(doi, headers={'accept': accept}).text
        k, t, v = self.parse_entry(r.strip(" "))
        self.entries[k] = bibentry(k, t, v)
        print(bibentry(k, t, v))

    def write(self, filename):
        print("Fix bibliography.write()")
        pass

