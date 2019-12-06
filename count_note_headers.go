package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
)

type countedFile struct {
	filename string
	count    int
}

func (c countedFile) String() string {
	return fmt.Sprintf("%-5d %s", c.count, c.filename)
}

type countedFiles []countedFile

func (cf countedFiles) Less(i, j int) bool {
	return cf[i].count < cf[j].count
}

func (cf countedFiles) Swap(i, j int) {
	cf[i], cf[j] = cf[j], cf[i]
}

func (cf countedFiles) Len() int {
	return len(cf)
}

const (
	NoFilesGlobFail int = iota
	PassedPatternGlobFail
)

func main() {
	var files []string
	var err error
	if len(os.Args) == 1 {
		files, err = filepath.Glob("**/*.txt")
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(NoFilesGlobFail)
		}
	} else if len(os.Args) == 2 && strings.HasPrefix(os.Args[1], "*") {
		files, err = filepath.Glob(os.Args[1])
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(PassedPatternGlobFail)
		}
	} else {
		files = os.Args[1:]
	}

	minCount := 5
	symbols := map[string]string{
		"md":  "#",
		"txt": "#",
		"org": "*",
	}
	filterWords := []string{"book-", "logbook", "asmr", "gaming", "programming"}
	var countedFileList countedFiles
	for _, file := range files {
		hasFilterWord := false
		for _, fw := range filterWords {
			if strings.Contains(file, fw) {
				hasFilterWord = true
				break
			}
		}
		if hasFilterWord {
			continue
		}
		sym := symbols[path.Ext(file)]
		count, err := headerCount(file, sym)
		if err != nil {
			os.Exit(1)
		}
		if count > minCount {
			countedFileList = append(countedFileList, countedFile{file, count})
		}
	}
	sort.Sort(sort.Reverse(countedFileList))

	for _, cf := range countedFileList {
		fmt.Println(cf)
	}
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
