package main

import (
	"fmt"
	"os"
	"path"
	"regexp"
	"strings"
)

func main() {
	fn := ""
	if len(os.Args) > 1 {
		fn = strings.Join(os.Args[1:], " ")
	} else {
		fmt.Fprintln(os.Stderr, "usage: sanitise <filename>")
		os.Exit(1)
	}

	direc := path.Dir(fn)
	base := path.Base(fn)

	transforms := []func(string) string{
		strings.ToLower,
		limit_characters,
		reduce_multiple_dashes,
		remove_trailing_dashes,
	}

	ext := path.Ext(base)
	out := base[:len(base)-len(ext)]
	for _, transform := range transforms {
		out = transform(out)
	}
	fmt.Println(path.Join(direc, out+ext))
}

func limit_characters(s string) string {
	re := regexp.MustCompile("[^a-zA-Z0-9.-]")
	return re.ReplaceAllString(s, "-")
}

func reduce_multiple_dashes(s string) string {
	re := regexp.MustCompile("--+")
	return re.ReplaceAllString(s, "--")
}

func remove_trailing_dashes(s string) string {
	re := regexp.MustCompile("-$")
	return re.ReplaceAllString(s, "")
}
