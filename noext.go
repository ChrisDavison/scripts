// Noext prints a filename without its last extension
package main

import (
	"fmt"
	"log"
	"os"
	"path"
	"strings"
)

const usage = `"usage: noext <FILE>"`

func main() {
	if len(os.Args) < 2 {
		log.Fatal(usage)
	}
	filename := os.Args[1]
	fmt.Fprintln(os.Stdout, strings.TrimSuffix(filename, path.Ext(filename)))
}
