package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func main() {
	var offset int64 = 0
	var err error
	if len(os.Args) > 1 {
		offset, err = strconv.ParseInt(os.Args[1], 10, 64)
	}
	t := time.Now()
	offsetMonth := time.Month(int64(t.Month()) + offset)
	t = time.Date(t.Year(), offsetMonth, 1, 0, 0, 0, 0, t.Location())

	tmp := t
	delta_1d, err := time.ParseDuration("24h")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to parse timedelta: %v", err)
		os.Exit(1)
	}
	for tmp.Month() == t.Month() {
		fmt.Printf("- %v-%02v-%02v %v ~\n",
			t.Year(),
			int(t.Month()),
			t.Day(),
			t.Weekday().String()[:3],
		)
		t = t.Add(delta_1d)
	}
}
