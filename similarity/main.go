package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"regexp"
	"sort"
	"strings"
)

func main() {
	fn := os.Args[1]
	lines := readToLines(fn)
	var wordBuckets [][]string
	for _, line := range lines {
		uniques := lineToUniqueSanitisedWordlist(line)
		wordBuckets = append(wordBuckets, uniques)
	}
	for _, bucket := range wordBuckets {
		fmt.Println(bucket)
	}
	// similarities := calcSimilarityMatrix(lines)
	// // noZeros := removeZeroDist(similarities)
	// top := SimilarityList(similarities).GetTopN(10)
	// for _, val := range top {
	// 	fmt.Println(val)
	// }
}

func removeZeroDist(ss []SimilarityPair) []SimilarityPair {
	out := make([]SimilarityPair, 0)
	for _, pair := range ss {
		if pair.dist > 0.1 {
			out = append(out, pair)
		}
	}
	return out
}

type SimilarityList []SimilarityPair

func (ss SimilarityList) SortByDist(asc bool) {
	sort.Slice(ss, func(i, j int) bool {
		if asc {
			return ss[i].dist > ss[j].dist
		}
		return ss[i].dist < ss[j].dist
	})
}

func (ss SimilarityList) GetTopN(n int) []SimilarityPair {
	ss.SortByDist(true)
	return ss[:n]
}

func readToLines(fn string) []string {
	file_contents, err := ioutil.ReadFile(fn)
	if err != nil {
		fmt.Fprintf(os.Stderr, "err: %s\n", err)
	}
	bbuf := bytes.NewBuffer(file_contents)
	file_as_string := bbuf.String()
	lines := strings.Split(file_as_string, "\n")
	out := make([]string, 0)
	for _, line := range lines {
		if strings.HasPrefix(line, "- ") {
			trimmed := strings.TrimPrefix(line, "- ")
			untagged := removeTags(trimmed)
			out = append(out, untagged)
		}
	}
	return out
}

func removeTags(s string) string {
	rx, err := regexp.Compile("`#.*`")
	if err != nil {
		log.Fatal(err)
	}
	return rx.ReplaceAllString(s, "")
}

type SimilarityPair struct {
	s1, s2 string
	dist   float64
}

func (s SimilarityPair) String() string {
	return fmt.Sprintf("%.2f :: %v - %v", s.dist, s.s1, s.s2)
}

func calcSimilarityMatrix(ss []string) []SimilarityPair {
	out := make([]SimilarityPair, len(ss)*2)
	for i, line := range ss {
		for _, line2 := range ss[i+1:] {
			a, b := line, line2
			if strings.Compare(a, b) > 0 {
				a, b = b, a
			}
			p := SimilarityPair{line, line2, 0}
			p.CalcSimilarity()
			out = append(out, p)
		}
	}
	return out
}

func filterJunk(words []string) []string {
	junkWords := map[string]bool{
		"and": true,
		"the": true,
		"of":  true,
		"is":  true,
		"a":   true,
	}
	out := make([]string, 0)
	for _, word := range words {
		isJunk, _ := junkWords[word]
		if isJunk {
			continue
		}
		out = append(out, word)
	}
	return out
}

func getUniqueWords(words []string) map[string]bool {
	out := make(map[string]bool)
	for _, w := range words {
		out[w] = true
	}
	return out
}

func (s *SimilarityPair) CalcSimilarity() {
	s1words := strings.Split(strings.ToLower(s.s1), " ")
	s2words := strings.Split(strings.ToLower(s.s2), " ")
	s1filtered := filterJunk(s1words)
	s2filtered := filterJunk(s2words)

	uniques := getUniqueWords(s1filtered)
	matchingUniques := 0.0
	for _, word := range s2filtered {
		_, ok := uniques[word]
		if ok {
			matchingUniques += 1
		}
	}
	length := len(s.s1)
	if len(s.s2) > len(s.s1) {
		length = len(s.s2)
	}
	s.dist = matchingUniques / float64(length)
}

func lineToUniqueSanitisedWordlist(line string) []string {
	words := strings.Split(line, " ")
	rxNonAsciiNum, err := regexp.Compile("[^a-zA-Z0-9-]")
	if err != nil {
		log.Fatalf("Failed to compile nonAsciiNum regex: %v\n", err)
		os.Exit(1)
	}
	filteredWords := filterJunk(words)
	uniqueMap := make(map[string]bool)
	for _, w := range filteredWords {
		removedNonAscii := rxNonAsciiNum.ReplaceAllString(w, "")
		uniqueMap[removedNonAscii] = true
	}
	uniqueWords := make([]string, 0)
	for word, ok := range uniqueMap {
		if ok {
			uniqueWords = append(uniqueWords, word)
		}
	}
	return uniqueWords
}
