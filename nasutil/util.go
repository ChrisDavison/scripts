package main

import (
	"bytes"
	"os"
)

func splitEitherCRLF(data []byte, atEOF bool) (advance int, token []byte, err error) {
	if atEOF && len(data) == 0 {
		return 0, nil, nil
	}
	if i := bytes.IndexByte(data, '\n'); i >= 0 {
		// We have a full newline-terminated line.
		return i + 1, data[0:i], nil
	}
	if i := bytes.IndexByte(data, '\r'); i >= 0 {
		// We have a full newline-terminated line.
		return i + 1, data[0:i], nil
	}
	// If we're at EOF, we have a final, non-terminated line. Return it.
	if atEOF {
		return len(data), data, nil
	}
	// Request more data.
	return 0, nil, nil
}

func inList(word string, words []string) bool {
	for _, listWord := range words {
		if word == listWord {
			return true
		}
	}
	return false
}

func nasRoot() string {
	options := []string{
		"/media/nas/",
		"//DAVISON-NAS/918-share",
		"Y://",
	}
	for _, option := range options {
		s, _ := os.Stat(option)
		if s != nil && s.IsDir() {
			return option
		}
	}
	return ""
}
