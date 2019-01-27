package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"os"
)

func main() {
	data, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		log.Fatal("Error reading stdin")
	}
	lines := bytes.Split(data, []byte{'\n'})
	fmt.Println(lines[rand.Intn(len(lines))])
}
