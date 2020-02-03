package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"regexp"
	"sort"
	"strings"

	"github.com/bmatcuk/doublestar"
)

type countedFile struct {
	filename string
	count    int
}

func (c countedFile) String() string {
	return fmt.Sprintf("%-5d %s", c.count, c.filename)
}

func main() {
	files, err := getFiles(os.Args)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	symbols := map[string]string{
		"md":  "#",
		"txt": "#",
		"org": "*",
	}

	var countedFileList []countedFile
	for _, file := range files {
		sym := symbols[path.Ext(file)]
		count, err := headerCount(file, sym)
		if err != nil {
			os.Exit(1)
		}
		countedFileList = append(countedFileList, countedFile{file, count})
	}

	sort.Slice(
		countedFileList,
		func(i, j int) bool {
			return countedFileList[i].count > countedFileList[j].count
		},
	)

	minCount := 0
	// filterWords := []string{"book-", "logbook", "asmr", "gaming", "programming"}
	filterWords := []string{}
	for _, cf := range countedFileList {
		if containsAny(cf.filename, filterWords) || (minCount > 0 && cf.count > minCount) {
			continue
		}
		fmt.Println(cf)
	}
}

func containsAny(s string, filters []string) bool {
	for _, fw := range filters {
		if strings.Contains(s, fw) {
			return true
		}
	}
	return false
}

func headerCount(file, headerSymbol string) (int, error) {
	re := regexp.MustCompile(strings.Join([]string{"^", headerSymbol, "+", " "}, ""))
	noteTextBytes, err := ioutil.ReadFile(file)
	if err != nil {
		return 0, err
	}
	noteLines := bytes.Split(noteTextBytes, []byte{'\n'})
	var linesWithHeaders [][]byte
	for _, line := range noteLines {
		if re.Match(line) {
			linesWithHeaders = append(linesWithHeaders, line)
		}
	}
	return len(linesWithHeaders), nil
}

func getFiles(args []string) ([]string, error) {
	var files []string
	var err error
	if len(os.Args) == 1 {
		files, err = doublestar.Glob("**/*.txt")
		if err != nil {
			return []string{}, fmt.Errorf("Error globbing doublestar: %w", err)
		}
	} else if len(os.Args) > 1 {
		files = os.Args[1:]
	} else {
		files = os.Args[1:]
	}
	return files, nil
}
