package main

import (
	"crypto/md5"
	"fmt"
	"io"
	"os"
)

const usage = `usage: shortsha <FILE>`

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, usage)
		os.Exit(1)
	}
	filename := os.Args[1]
	f, err := os.Open(filename)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Couldn't open file")
		os.Exit(2)
	}
	defer f.Close()

	h := md5.New()
	if _, err := io.Copy(h, f); err != nil {
		fmt.Fprintln(os.Stderr, "Error copying file data to hash")
		os.Exit(3)
	}
	fmt.Fprintf(os.Stderr, "%x", h.Sum(nil))
}
