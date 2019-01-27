package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	path := os.Getenv("PATH")
	fmt.Fprintln(
		os.Stdout,
		strings.Replace(
			path,
			string(os.PathListSeparator),
			"\n",
			-1,
		),
	)

}
