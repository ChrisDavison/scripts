package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"
)

// command-line arguments
var (
	prefix  = flag.String("prefix", "", "Prefix to prepend to sequential number")
	suffix  = flag.String("suffix", "", "Suffix to append to sequential number")
	verbose = flag.Bool("verbose", false, "Show files renamed")
)

func renameFilesInDir(directory, prefix, suffix string, verbose bool) {
	files, err := ioutil.ReadDir(directory)
	if err != nil {
		log.Fatalf("Reading dir %v", err)
	}
	i := 0
	for _, fileinfo := range files {
		if fileinfo.IsDir() {
			continue
		}
		ext := path.Ext(fileinfo.Name())
		newName := fmt.Sprintf("%s%04d%s%s", prefix, i, suffix, ext)
		i++
		if verbose {
			fmt.Printf("%s -> %s\n", fileinfo.Name(), newName)
		}
		os.Rename(fileinfo.Name(), newName)
	}
}

func main() {
	flag.Parse()
	if *prefix != "" {
		*prefix = *prefix + "--"
	}
	if *suffix != "" {
		*suffix = "--" + *suffix
	}
	for _, directory := range flag.Args() {
		renameFilesInDir(directory, *prefix, *suffix, *verbose)
	}

}
