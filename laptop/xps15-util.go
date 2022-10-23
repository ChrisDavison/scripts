package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
)

const helpStr string = `xps15-util
utilities for my xps15 laptop

usage:
	xps15-util brightness up|down|show
	xps15-util volume up|down|show|mute
`

func help() {
	fmt.Println(helpStr)
	os.Exit(1)
}

func readIntFromFile(filename string) (int64, error) {
	f, err := os.Open(filename)
	if err != nil {
		return 0, err
	}
	valBytes, err := ioutil.ReadAll(f)
	val, err := strconv.ParseInt(string(valBytes), 64, 10)
	return val, nil
}

func inList(val string, list []string) bool {
	for _, v := range list {
		if val == v {
			return true
		}
	}
	return false
}

func main() {
	if len(os.Args) < 2 {
		help()
	}
	args := os.Args[1:]
	cmd := args[0]

	if inList(cmd, []string{"brightness", "bright", "b"}) {
		brightness(args[1:])
	} else if inList(cmd, []string{"volume", "vol", "v"}) {
		volume(args[1:])
	} else {
		help()
	}
}
