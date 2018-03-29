// Markdown Link Checker
package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strings"
	"sync"
)

func main() {
	fmt.Println("vim-go")
	if len(os.Args) == 1 {
		fmt.Printf("usage:\n\t%v <dir>\n", os.Args[0])
	}
	c := make(<-chan checkedLine)
	var wg sync.WaitGroup
	go checkDoc(os.Args[1], c, wg)
	doc := <-c
	fmt.Printf("%v\n", doc)
	// Set off a goroutine for every file
	// ...for each goroutine, set off a goroutine for every link

	// checkFile function takes a channel
	// ...channel sends back a list of lines with problematic links
	// ...if the channel or file open had issue, return an error
}

type checkedLine struct {
	linum      int
	brokenLink string
}

func checkDoc(fn string, c <-chan checkedLine, wg sync.WaitGroup) error {
	contents, err := ioutil.ReadFile(fn)
	if err != nil {
		return err
	}
	buf := bytes.NewBuffer(contents)
	lines := strings.Split(buf.String(), "\n")
	out := make([]checkedLine, 0, len(lines))
	wg.Add(1)
	for i, line := range lines {
		for _, link := range linksInLine(line) {
			checker := linkIsFineWeb
			if isLocalLink(link) {
				checker = linkIsFineLocal
			}
			if !checker(link) {
				out = append(out, checkedLine{i, link})
			}
		}

	}
	wg.Done()
	return nil
}

func linksInLine(l string) []string {
	rx := regexp.MustCompile(`\[.+\]\((.+)\)|\[.+\]: (.+)`)
	return rx.FindAllString(l, -1)
}

func isLocalLink(l string) bool {
	rx := regexp.MustCompile(`\./(.*)\.(png|jpg|jpeg|md)`)
	return rx.MatchString(l)
}

func linkIsFineWeb(s string) bool {
	return false
}

func linkIsFineLocal(s string) bool {
	if _, err := os.Stat(s); os.IsNotExist(err) {
		return false
	}
	return true
}
