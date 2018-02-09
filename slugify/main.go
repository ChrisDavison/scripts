package main

import (
	"fmt"
	"strings"

	kingpin "gopkg.in/alecthomas/kingpin.v2"

	"github.com/gosimple/slug"
)

func main() {
	sentence := kingpin.Arg("sentence", "String to slugify").Required().Strings()
	kingpin.Parse()
	joined := strings.Join(*sentence, " ")
	fmt.Println(slug.Make(joined))
}
