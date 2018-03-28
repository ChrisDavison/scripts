package main

import (
	"fmt"
	"os"
	"regexp"
)

type WalkerWithRegex struct {
	pattern string
}

func (w WalkerWithRegex) Walk(path string, info os.FileInfo, err error) error {
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failure accessing path %s: %v\n", path, err)
		return err
	}
	rx, err := regexp.Compile(w.pattern)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error compiling regex: %s\n", err)
		return err
	}
	if !rx.MatchString(path) {
		return nil
	}
	fixed, err := filenameFixer(path, w.pattern)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error fixing path %s: %s\n", path, err)
		return err
	}
	msg := fmt.Sprintf("%s\n\tto\n%s\nRename? [Y/N]", path, fixed)
	rsp, err := getYesNo(msg)
	if err != nil {
		return err
	}
	if !rsp {
		return nil
	}
	if err := os.Rename(path, fixed); err != nil {
		fmt.Fprintf(os.Stderr, "Error renaming %s: %s\n", path, err)
		return err
	}
	return nil

}

func filenameFixer(s string, r string) (string, error) {
	rx, err := regexp.Compile(r)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error compiling regexp: %s\n", err)
		return "", err
	}
	return rx.ReplaceAllString(s, ""), nil
}
