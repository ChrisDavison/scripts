package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strings"

	"github.com/antzucaro/matchr"
)

func main() {
	fn := os.Args[1]
	lines := readToLines(fn)
	similarities := calcSimilarityMatrix(lines)
	top10 := getTopNSimilarities(similarities, 10)
	for _, val := range top10 {
		fmt.Println(val)
	}
}

func getTopNSimilarities(ss []SimilarityPair, n int) []SimilarityPair {
	sort.Slice(ss, func(i, j int) bool {
		return ss[i].dist > ss[j].dist
	})
	j := 0
	out := make([]SimilarityPair, 10)
	for _, pair := range ss {
		if j > n {
			break
		}
		if pair.dist == 0 {
			continue
		}
		j += 1
		out = append(out, pair)
	}
	return out
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
			out = append(out, strings.TrimPrefix(line, "- "))
		}
	}
	return out
}

type SimilarityPair struct {
	s1, s2 string
	dist   float64
}

func (s SimilarityPair) String() string {
	return fmt.Sprintf("%.2f\n\t%v\n\t%v", s.dist, s.s1, s.s2)
}

func calcSimilarityMatrix(ss []string) []SimilarityPair {
	out := make([]SimilarityPair, len(ss)*2)
	for _, line := range ss {
		for _, line2 := range ss {
			if line == line2 {
				continue
			}
			if line == "" || line2 == "" {
				continue
			}
			sim := matchr.Jaro(line, line2)
			if sim == 0 {
				continue
			}
			out = append(out, SimilarityPair{line, line2, sim})
		}
	}
	return out
}
