// Noext prints a filename without its last extension
package main

import (
	"fmt"
	"os"
	"path"
	"strings"
)

const usage = `"usage: noext <FILE>"`

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, usage)
		os.Exit(1)
	}
	filename := os.Args[1]
	fmt.Fprintln(os.Stdout, strings.TrimSuffix(filename, path.Ext(filename)))
}
