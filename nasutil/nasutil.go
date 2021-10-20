package main

import (
	"fmt"
	"net/url"
	"os"
)

const USAGE = `usage:
    nasutil list
    nasutil download
    nasutil add <url>|<md_link>`
const USAGE_LONG = `usage: nasutil CMD

command               alias   description
---------------------------------------------
list                  l       show urls waiting to be downloaded
download              dl,d    use youtube-dl to download each url
add <url>|<md_link>   a       add a url to the list`

const (
	ERR_NO_COMMAND = iota + 1
	ERR_ADD_BAD_URL
	ERR_ADD_NO_URL
	ERR_COULDNT_OPEN_FILE
	ERR_COULDNT_WRITE_FILE
)

const VERSION = "2021-10-16"

func main() {
	args := os.Args[1:]
	if len(args) == 0 {
		fmt.Println(USAGE)
		os.Exit(ERR_NO_COMMAND)
	}

	dls := GetDownloadList()
	fmt.Printf("%d URLs to download. %d previously failed.\n", len(dls.urls), len(dls.failures))

	command := args[0]
	if inList(command, []string{"list", "l"}) {
		dls.list()
	} else if inList(command, []string{"download", "dl", "d"}) {
		dls.downloadEach()
		dls.SaveFiles()
	} else if inList(command, []string{"help", "h", "--help"}) {
		fmt.Println(USAGE_LONG)
	} else if inList(command, []string{"v", "version", "--version"}) {
		fmt.Printf("nasutil %v\n", VERSION)
	} else if inList(command, []string{"add", "a"}) {
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
		dls.SaveFiles()
	} else {
		fmt.Println(USAGE)
	}
}
