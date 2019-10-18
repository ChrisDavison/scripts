package main

import (
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"
)

// Version is the major.minor.patch version number
var Version string

// Build is the git commit hash when built
var Build string

func init() {
	rand.Seed(time.Now().UnixNano())
}

func randomChoice(ls []string) string {
	return ls[rand.Intn(len(ls))]
}

func main() {
	withCaps := false
	for _, arg := range os.Args {
		if arg == "-c" {
			withCaps = true
		}
		if arg == "-v" {
			fmt.Printf("Animalhash %v (%v)\n", Version, Build[:8])
			os.Exit(1)
		}
	}

	animals := strings.Split(ANIMALS, "\n")
	adjectives := strings.Split(ADJECTIVES, "\n")
	colours := strings.Split(COLOURS, "\n")

	animal := randomChoice(animals)
	adjective := randomChoice(adjectives)
	colour := randomChoice(colours)

	sentence := fmt.Sprintf("%v %v %v", adjective, colour, animal)
	if withCaps {
		sentence = strings.Title(sentence)
	}
	fmt.Println(strings.Replace(sentence, " ", "", -1))
}
