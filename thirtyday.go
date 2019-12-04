// thirtyday generates an outline for a '30 day challenge'
package main

import (
	"fmt"
	"os"
	"time"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	title = kingpin.Arg("title", "Title of challenge").Required().String()
	shift = kingpin.Arg("d", "How many days till start").Uint()
)

func main() {
	kingpin.Parse()
	var err error
	t := time.Now()
	delta_1d, err := time.ParseDuration("24h")
	for i := uint(0); i < *shift; i++ {
		t = t.Add(delta_1d)
	}
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to parse timedelta: %v", err)
		os.Exit(1)
	}
	fmt.Println(*title)
	fmt.Printf("[")
	for i := 0; i < 30; i++ {
		day := t.Weekday()
		fmt.Printf("%c", day.String()[0])
		if day == time.Sunday {
			fmt.Printf(" ")
		}
		t = t.Add(delta_1d)
	}
	fmt.Println("]")
}
