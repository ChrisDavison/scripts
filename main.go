package main

import (
	"crypto/sha1"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) == 1 {
		fmt.Println("usage: shortsha <file>")
		return
	}
	f, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatalf("Couldn't open file: %v\n", err)
	}
	var n int64 = 8
	if len(os.Args) > 2 {
		n, err = strconv.ParseInt(os.Args[2], 10, 8)
		if err != nil {
			log.Fatalf("Error parsing number of chars: %v\n", err)
		}
	}
	data, err := ioutil.ReadAll(f)
	if err != nil {
		log.Fatalf("Couldn't read file: %v\n", err)
	}
	sum := sha1.Sum(data)
	shaStr := fmt.Sprintf("%x", sum)
	fmt.Println(shaStr[:n])
}
