// Package main provides ...
package main

import (
	"flag"
	"fmt"
	"strings"
	"time"
)

const day = time.Hour * 24

var dated = flag.Bool("d", false, "Show start and end dates")
var shift = flag.Int("s", 0, "Number of days to shift start by")

func thirtyday(start time.Time, title string, dated bool) {
	days := []string{"M", "T", "W", "T", "F", "S", "S "}
	daycal := ""
	startstr := start.Format("2006-01-02")
	for i := 0; i < 30; i++ {
		weekday := start.Weekday()
		daycal += string(days[weekday])
		start = start.Add(day)
	}
	endstr := start.Format("2006-01-02")

	if len(title) > 0 {
		fmt.Println(title)
	}
	if dated {
		dots := strings.Repeat(".", len(daycal)-22)
		dateheader := fmt.Sprintf("%s %s %s", startstr, dots, endstr)
		fmt.Println(dateheader)
	}
	fmt.Println(daycal)
}

func main() {
	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(), "usage:\n\tthirtyday [-s <n>] [-d] <TITLE>...\n\nFlags:\n")
		flag.PrintDefaults()
	}

	flag.Parse()

	start := time.Now()
	for i := 0; i < *shift; i++ {
		start = start.Add(day)
	}

	thirtyday(start, strings.Join(flag.Args(), " "), *dated)
}
