package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

// Bookmark represents a plaintext bookmark
type Bookmark struct {
	title string
	url   string
	date  string
	tags  []string
	notes string
}

func (b Bookmark) String() string {
	var out string
	out += b.title
	if len(b.date) > 0 {
		out += " (" + b.date + ")\n"
	}
	out += b.url + "\n"
	var tags []string
	for _, tag := range b.tags {
		tags = append(tags, "@"+tag)
	}
	out += strings.Join(tags, " ")
	return out
}

func parseBookmark(filename string) (Bookmark, error) {
	contents, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading %v\n: %v", filename, err)
		return Bookmark{}, err
	}
	var title string
	var url string
	var date string
	var tags []string
	var notes string
	for _, line := range strings.Split(string(contents), "\n") {
		parts := strings.Split(line, ": ")
		if len(parts) == 1 {
			notes += parts[0]
			continue
		}
		key, value := parts[0], parts[1]
		if key == "title" {
			title = value
		} else if key == "url" {
			url = value
		} else if key == "date" {
			date = value
		} else if key == "tags" {
			tags = strings.Split(value, " ")
		} else {
			fmt.Fprintf(os.Stderr, "Unrecognised key: %s", key)
		}
	}
	return Bookmark{title, url, date, tags, notes}, nil
}
