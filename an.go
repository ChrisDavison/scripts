package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"sort"
	"strings"
)

const usage = `an <command> [<files>...]

AnalyseNotes. Various utilities for summarising notes.

commands:
    complexity   -- heuristic for complexity of structure
    headercount  -- how many headers in the file
    size         -- sorted by wordcount
    structure    -- outline of headers in the file (maybe with wordcount)
`

func noteSize(files []string) {
	for _, fname := range files {
		info, err := os.Lstat(fname)
		if err != nil {
			log.Fatal(err)
		}
		kb := float64(info.Size()) / 1024.0
		fmt.Printf("%.2fkb %s\n", kb, fname)
	}
}

func noteComplexity(files []string) {
	type fileComplexity struct {
		filename   string
		complexity float32
	}
	complexities := make([]fileComplexity, 0, 100)
	for _, fname := range files {
		if !strings.HasSuffix(fname, ".md") {
			continue
		}
		bcontents, err := ioutil.ReadFile(fname)
		if err != nil {
			log.Fatal("Headercount ReadFile ", fname)
		}
		contents := string(bcontents)
		lines := strings.Split(contents, "\n")
		complexitySum := 0
		headerCount := 0
		for _, line := range lines {
			firstWord := strings.Split(line, " ")[0]
			if len(firstWord) == 0 || firstWord != strings.Repeat("#", len(firstWord)) {
				continue
			}
			complexitySum += len(firstWord)
			headerCount++
		}
		complexity := float32(complexitySum) / float32(headerCount)
		if complexitySum == 0 || complexity < 1 {
			complexity = 0
		}
		complexities = append(complexities, fileComplexity{fname, complexity})
	}
	sort.Slice(complexities, func(i, j int) bool {
		return complexities[i].complexity > complexities[j].complexity
	})
	for _, complexity := range complexities {
		fmt.Printf("%.2f %s\n", complexity.complexity, complexity.filename)
	}
}

func noteHeaderCount(files []string) {
	type countedFile struct {
		fname string
		count int
	}
	countedFiles := make([]countedFile, 0, len(files))
	for _, fname := range files {
		stat, err := os.Lstat(fname)
		if err != nil {
			log.Fatal("HeaderCount Lstat ", fname)
		}
		if stat.IsDir() || !strings.HasSuffix(fname, ".md") {
			continue
		}
		bcontents, err := ioutil.ReadFile(fname)
		if err != nil {
			log.Fatal("Headercount ReadFile ", fname)
		}
		contents := string(bcontents)
		lines := strings.Split(contents, "\n")
		headerCount := 0
		for _, line := range lines {
			if strings.HasPrefix(line, "#") {
				headerCount++
			}
		}
		countedFiles = append(countedFiles, countedFile{fname, headerCount})
	}
	sort.Slice(countedFiles, func(i, j int) bool {
		return countedFiles[i].count > countedFiles[j].count
	})
	for _, countedFile := range countedFiles {
		fmt.Printf("%d %s\n", countedFile.count, countedFile.fname)
	}
}

func noteStructure(files []string) {
	for _, fname := range files {
		if !strings.HasSuffix(fname, ".md") {
			continue
		}
		bcontents, err := ioutil.ReadFile(fname)
		if err != nil {
			log.Fatal("Headercount ReadFile ", fname)
		}
		contents := string(bcontents)
		lines := strings.Split(contents, "\n")
		header := fname
		headerCount := 0
		structureOfFile := ""
		for _, line := range lines {
			if strings.HasPrefix(line, "#") {
				headerCount++
				structureOfFile += fmt.Sprintf("    %s\n", line)
			}
		}
		fmt.Printf("%s - %d headers\n", header, headerCount)
		fmt.Println(structureOfFile)
	}
}

func globFiles(ext string) []string {
	infos, err := ioutil.ReadDir(".")
	if err != nil {
		log.Fatal(err)
	}
	files := make([]string, 0, 100)
	for _, info := range infos {
		if !info.IsDir() && strings.HasSuffix(info.Name(), ext) {
			files = append(files, info.Name())
		}
	}
	return files
}

func main() {
	args := os.Args[1:]
	if len(args) == 0 {
		fmt.Println(usage)
		os.Exit(0)
	}
	command := args[0]
	files := args[1:]
	if len(files) == 0 {
		files = globFiles(".md")
	}
	switch command {
	case "size":
		noteSize(files)
	case "complexity":
		noteComplexity(files)
	case "headercount", "count":
		noteHeaderCount(files)
	case "structure":
		noteStructure(files)
	default:
		fmt.Println(usage)
		os.Exit(1)
	}
}
