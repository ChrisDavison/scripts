// Markdown Link Checker
package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strings"
)

func main() {
	fmt.Println("vim-go")
	if len(os.Args) == 1 {
		fmt.Printf("usage:\n\t%v <dir>\n", os.Args[0])
	}
	// Set off a goroutine for every file
	// ...for each goroutine, set off a goroutine for every link

	// checkFile function takes a channel
	// ...channel sends back a list of lines with problematic links
	// ...if the channel or file open had issue, return an error
}

func checkDoc(fn string, c <-chan string) error {
	contents, err := ioutil.ReadFile(fn)
	if err != nil {
		return err
	}
	buf := bytes.NewBuffer(contents)
	lines := strings.Split(buf.String(), "\n")
	// out := make([]string, 0, len(lines))
	for _, line := range lines {
		for _, link := range linksInLine(line) {
			fmt.Println(link)
		}

	}
	return nil
}

func linksInLine(l string) []string {
	rx := regexp.MustCompile(`[.+]\((.+)\)|[]: (.+)`)
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
