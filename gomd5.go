package main

import (
	"crypto/md5"
	"fmt"
	"io"
	"log"
	"os"
)

const usage = `usage: shortsha <FILE>`

func main() {
	if len(os.Args) < 2 {
		log.Fatal(usage)
	}
	filename := os.Args[1]
	f, err := os.Open(filename)
	if err != nil {
		log.Fatal("Couldn't open file")
	}
	defer f.Close()

	h := md5.New()
	if _, err := io.Copy(h, f); err != nil {
		log.Fatal("Error copying file data to hash")
	}
	fmt.Fprintf(os.Stderr, "%x", h.Sum(nil))
}
