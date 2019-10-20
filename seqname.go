package main

import (
	"flag"
	"fmt"
	"os"
	"path"
	"path/filepath"
)

func main() {
	prefix := flag.String("prefix", "", "Prefix to insert before number")
	suffix := flag.String("suffix", "", "Suffix to insert before number")
	verbose := flag.Bool("v", false, "Show files moved/renamed")
	flag.Parse()
	if *prefix != "" {
		*prefix = *prefix + "--"
	}
	if *suffix != "" {
		*suffix = "--" + *suffix
	}
	dirs := flag.Args()
	for _, direc := range dirs {
		renameFilesInDir(direc, *prefix, *suffix, *verbose)
	}
}

func renameFilesInDir(dir, prefix, suffix string, verbose bool) {
	glob, _ := filepath.Glob(dir + `/*`)
	for i, fpath := range glob {
		parent, _ := path.Split(fpath)
		ext := path.Ext(fpath)
		newFname := fmt.Sprintf("%v%v%v%v", prefix, i, suffix, ext)
		newFpath := path.Join(parent, newFname)
		if verbose {
			fmt.Printf("%v -> %v\n", fpath, newFpath)
		}
		os.Rename(fpath, newFpath)
	}
}
