package main

import "fmt"
import "os"
import "io/ioutil"
import "path"
import "strings"

type Bookmark struct {
    title string
    url string
    date string
    tags []string
    hash string
    notes string
}

func (b Bookmark) String() string {
    var out string
    out += b.title
    if len(b.date) > 0 {
        out += " (" + b.date + ")\n"
    } 
    out += "\n"
    out += b.url + "\n"
    // out += b.hash + "\n"
    var hashtags []string
    for _, tag := range b.tags {
        hashtags = append(hashtags, "#" + tag)
    }
    out += strings.Join(hashtags, " ")
    return out
}

func main() {
    bookmarksDir := os.Getenv( "HOME" )
    bm := path.Join(bookmarksDir, "Dropbox", "bookmarks")
    dirContents, err := ioutil.ReadDir(bm)
    if err != nil {
        fmt.Fprintln(os.Stderr, "%v\n")
        return
    }
    matchingBookmarks := make([]Bookmark, 0, 1000)
    var queries []string
    if len(os.Args) > 1 {
        queries = os.Args[1:]
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
                if matches == len(queries){
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
    var hash string
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
        } else if key == "hash" {
            hash = value
        } else if key == "tags" {
            tags = strings.Split(value, " ")
        }
    }
    return Bookmark{title, url, date, tags, hash, notes}, nil
}
