package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path"
)

const USAGE = `Display and search bookmarks in $BOOKMARKS

usage:
	# Show this message
	bookmarks -h|--help

	# List bookmarks (optionally with tags matching query)
	bookmarks query...
`

func main() {
	bookmarksDir := os.Getenv("HOME")
	bm := path.Join(bookmarksDir, "Dropbox", "bookmarks")
	dirContents, err := ioutil.ReadDir(bm)
	if err != nil {
		fmt.Fprintln(os.Stderr, "%v\n")
		return
	}
	matchingBookmarks := make([]Bookmark, 0, 1000)
	var queries []string
	help := false
	for _, arg := range os.Args[1:] {
		if arg == "-h" || arg == "--help" {
			help = true
		} else {
			queries = append(queries, arg)
		}
	}
	if help {
		fmt.Println(USAGE)
		os.Exit(0)
	}
	for _, info := range dirContents {
		if info.IsDir() {
			continue
		}
		if len(info.Name()) == 0 {
			continue
		}
		fullpath := path.Join(bm, info.Name())
		parsed, err := parseBookmark(fullpath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error with %v: %v", info.Name(), err)
			continue
		}
		matches := 0
		if len(queries) > 0 {
			for _, required := range queries {
				for _, tag := range parsed.tags {
					if tag == required {
						matches += 1
					}
				}
				if matches == len(queries) {
					matchingBookmarks = append(matchingBookmarks, parsed)
				}
			}
		} else {
			matchingBookmarks = append(matchingBookmarks, parsed)
		}

	}

	for i, bmRust := range matchingBookmarks {
		fmt.Println(i, ":", bmRust, "\n")
	}
}
