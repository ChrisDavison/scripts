package main

import (
	"fmt"
	"os"
	"strconv"
)

const USAGE = `chesstc - Calculate expected chess game time.

usage: chesstc <BASE> <INCREMENT>

This calculates the expected duration of a chess game (Min:Sec) for a given
base and increment; e.g. 5+0 should take approx 10 minutes.

Assumes 40 moves, using a given base and increment.  Each player will have
half of this duration each.`

func main() {
	for _, a := range os.Args {
		if a == "-h" || a == "--help" {
			fmt.Println(USAGE)
			os.Exit(0)
		}
	}

	if len(os.Args) < 3 {
		fmt.Fprintln(os.Stderr, "usage: chesstc <base> <increment>")
		os.Exit(-1)
	}
	base, err := strconv.ParseInt(os.Args[1], 10, 64)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to parse base `%s`", os.Args[1])
		os.Exit(1)
	}
	increment, err := strconv.ParseInt(os.Args[2], 10, 64)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to parse increment `%s`", os.Args[2])
		os.Exit(2)
	}
	totalSec := base*60 + increment*40*2

	min := int(totalSec / 60)
	remsec := int(int(totalSec) - min*60)
	fmt.Printf("%d:%d\n", min, remsec)
}
