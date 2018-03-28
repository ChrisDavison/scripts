package main

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	pattern := "[0-9]+--"
	var dir string = os.Args[1]
	if len(os.Args) == 1 {
		fmt.Fprintf(os.Stderr, "usage:\n\t%s [<regex>] <dir>\n", os.Args[0])
		os.Exit(1)
	} else if len(os.Args) == 3 {
		pattern = os.Args[1]
		dir = os.Args[2]
	} else {
		dir = os.Args[1]
	}

	w := WalkerWithRegex{pattern}
	err := filepath.Walk(dir, w.Walk)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failure walking path: %s\n", err)
	}
}

func getYesNo(s string) (bool, error) {
	var response string
	fmt.Printf("%s", s)
	_, err := fmt.Scanln(&response)
	if err != nil {
		return false, err
	}
	if len(response) < 1 {
		fmt.Fprintf(os.Stderr, "Response too short. Yes/No please.")
		return false, errors.New("Response too short")
	}
	lowered := strings.ToLower(response)
	return lowered[0] == 'y', nil
}
