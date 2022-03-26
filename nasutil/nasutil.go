package main

import (
	"fmt"
	"net/url"
	"os"
)

const USAGE = `usage:
    nasutil list
    nasutil failed
    nasutil download
    nasutil add <url>|<md_link>
    nasutil empty
    nasutil emptyfailed
    `
const USAGE_LONG = `usage: nasutil CMD

commands ([shortalias]):
    list [l]                  show urls waiting to be downloaded
    failed [f]                show urls that have failed
    download [dl,d]           use youtube-dl to download each url
    add <url>|<md_link> [a]   add a url to the listFailed
    empty [e]                 clear list to be downloaded
    emptyfailed [ef]          clear list of previous failures
    `

const (
	ERR_NO_COMMAND = iota + 1
	ERR_ADD_BAD_URL
	ERR_ADD_NO_URL
	ERR_COULDNT_OPEN_FILE
	ERR_COULDNT_WRITE_FILE
)

const VERSION = "2022-03-26"

func main() {
	args := os.Args[1:]
	if len(args) == 0 {
		fmt.Println(USAGE)
		os.Exit(ERR_NO_COMMAND)
	}

	dls := GetDownloadList()

	command := args[0]
	if inList(command, []string{"l", "list", "--list"}) {
		dls.summary()
		dls.list()
	} else if inList(command, []string{"f", "failed", "--failed"}) {
		dls.summary()
		dls.listFailed()
	} else if inList(command, []string{"d", "download", "--download", "dl"}) {
		dls.summary()
		dls.downloadEach()
	} else if inList(command, []string{"h", "help", "--help"}) {
		fmt.Println(USAGE_LONG)
	} else if inList(command, []string{"v", "version", "--version"}) {
		fmt.Printf("nasutil %v\n", VERSION)
	} else if inList(command, []string{"e", "empty", "--empty"}) {
		dls.EmptyDownloads()
	} else if inList(command, []string{"ef", "emptyfailed", "--empty-failed"}) {
		dls.EmptyFailures()
	} else if inList(command, []string{"add", "a"}) {
		dls.summary()
		if len(args) == 1 {
			fmt.Fprintln(os.Stderr, "USAGE: nasutil add <url>|<mdlink>")
			os.Exit(ERR_ADD_NO_URL)
		}
		url, err := url.ParseRequestURI(args[1])
		if err != nil {
			fmt.Printf("Url doesn't seem to be valid: `%v`: %v\n", os.Args[1], err)
			os.Exit(ERR_ADD_BAD_URL)
		}
		dls.add(url.String())
	} else {
		fmt.Println(USAGE)
	}
	dls.Save()
}
