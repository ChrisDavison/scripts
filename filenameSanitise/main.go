package main

import (
	"fmt"
	"path"
	"strings"

	kingpin "gopkg.in/alecthomas/kingpin.v2"

	"github.com/gosimple/slug"
)

func main() {
	filename := kingpin.Arg("filename", "Filename to sanitise").Required().String()
    kingpin.Parse()
	ext := path.Ext(*filename)
	filenameNoExt := strings.TrimSuffix(*filename, ext)
	slugged := slug.Make(filenameNoExt)
	sluggedNoUnderline := strings.Replace(slugged, "_", "-", -1)
	sluggedNoTrailingDash := strings.TrimSuffix(sluggedNoUnderline, "-")
	fmt.Printf("%s%s\n", sluggedNoTrailingDash, ext)
}
