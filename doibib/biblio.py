import re
import requests
import sys

rType = re.compile('@([a-zA-Z0-9]+)[{]')
rCiteCode = re.compile('@.*?[{](.*?),')
tags = ['author', 'journal', 'title', 'year', 'url', 'publisher',
        'series', 'type', 'chapter', 'pages', 'address', 'edition',
        'month', 'note', 'school', 'howpublished', 'editor',
        'organization', 'volume', 'institution']

rTag = re.compile('(' + "|".join(tags) + ')\s?=\s?([{].*?[}][,} ])')


class bibentry:
    def __init__(self, citeCode, entrytype, details):
        self.entrytype = entrytype
        self.citeCode = citeCode
        self.details = details

    def __str__(self):
        out = "{:<18}[{}]\n".format(self.citeCode, self.entrytype)
        for key, value in self.details:
            out += "{:>15} - {}\n".format(key, value.strip(", "))
        out += "-"*80
        return out

    def __file_repr__(self):
        articleType = "@{}".format(self.citeCode)
        out = ""
        for k, v in self.details:
            if k and v:
                out += "{} = {}, ".format(k, v.strip(", "))
        out = articleType + "{" + out[:-2] + "}"
        return out


class bibliography:
    def __init__(self, fn):
        self.fn = fn
        self.entries = {}
        try:
            self.parse_file(fn)
        except Exception as E:
            print("Failed parsing.")
            sys.exit(E)

    def parse_file(self, filename):
        # May need to modify this to join all lines in a bib entry.
        # Right now this presumes that each bib entry is a single line
        # so make it that way.
        lines = [line for line in open(filename)]
        lines = lines[5:]  # Skip Mendeley's stuff...

        for line in lines:
            try:
                k, t, v = self.parse_entry(line)
            except:
                continue
            if k and t and v:
                self.entries[k] = bibentry(k, t, v)

    def parse_entry(self, line):
        try:
            entrytype = re.match(rType, line).groups()[0]
            if entrytype == "":
                return
            citeCode = re.match(rCiteCode, line).groups()[0]

            matches = re.findall(rTag, line)
            out = [match for match in matches]

            return citeCode, entrytype, out
        except:
            return

    def search(self, searchword):
        for citeCode, entry in self.entries.items():
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
        accept = 'text/x-bibliography; style=bibtex'
        if not doi.startswith("http://"):
            doi = "http://dx.doi.org/" + doi
        r = requests.get(doi, headers={'accept': accept}).text
        k, t, v = self.parse_entry(r.strip(" "))
        self.entries[k] = bibentry(k, t, v)
        print(bibentry(k, t, v))

    def write(self, filename):
        with open(filename, 'w') as f:
            for bibentry in self.entries.values():
                f.write(bibentry.__file_repr__())
                f.write("\n\n")
            f.write("\n")
