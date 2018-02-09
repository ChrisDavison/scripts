package main

import (
	"crypto/sha1"
	"fmt"
	"io/ioutil"
	"log"
	"os"

	kingpin "gopkg.in/alecthomas/kingpin.v2"
)

func main() {
	file := kingpin.Arg("file", "File to generate hash for").Required().String()
	n := kingpin.Flag("chars", "Number of hash characters to return").
		Short('n').Default("8").Int()
	kingpin.Parse()
	f, err := os.Open(*file)
	if err != nil {
		log.Fatalf("Couldn't open file: %v\n", err)
	}
	data, err := ioutil.ReadAll(f)
	if err != nil {
		log.Fatalf("Couldn't read file: %v\n", err)
	}
	sum := sha1.Sum(data)
	shaStr := fmt.Sprintf("%x", sum)
	fmt.Println(shaStr[:*n])
}
