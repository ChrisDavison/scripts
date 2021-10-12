package main

import (
	"bufio"
	"bytes"
	"fmt"
	"net/url"
	"os"
	"os/exec"
	"path"
	"regexp"
	"strings"
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

func main() {
	args := os.Args[1:]
	if len(args) == 0 {
		fmt.Println(USAGE)
		os.Exit(ERR_NO_COMMAND)
	}
	dls := getContentsOfNasFile("to-download.txt")
	command := args[0]
	if inList(command, []string{"list", "l"}) {
		list(dls)
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
		add(dls, fmt.Sprintf("%s", url))
	} else if inList(command, []string{"download", "dl", "d"}) {
		downloadEach(dls)
	} else if inList(command, []string{"help", "h", "--help"}) {
		fmt.Println(USAGE_LONG)
	} else {
		fmt.Println(USAGE)
	}
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

// Rather than a slice, return a map of string -> true
// so that we reject duplicates.
func getContentsOfNasFile(filename string) map[string]bool {
	f, err := os.Open(path.Join(nasRoot(), filename))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Couldn't open `%v`: %v\n", filename, err)
		os.Exit(ERR_COULDNT_OPEN_FILE)
	}
	defer f.Close()
	bufreader := bufio.NewScanner(f)
	lines := make(map[string]bool, 0)
	for bufreader.Scan() {
		lines[bufreader.Text()] = true
	}
	return lines
}

func writeListOfUrls(urls map[string]bool, filename string) {
	f, err := os.Create(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Couldn't open `%v`: %v\n", filename, err)
		os.Exit(ERR_COULDNT_OPEN_FILE)
	}
	defer f.Close()
	fbuf := bufio.NewWriter(f)
	defer fbuf.Flush()
	for url := range urls {
		_, err := fbuf.WriteString(url + "\n")
		if err != nil {
			fmt.Fprintf(os.Stderr, "Couldn't write url `%v` to file: %v", url, err)
			os.Exit(ERR_COULDNT_WRITE_FILE)
		}
	}
}

func emptyDownloads() {
	blank := make(map[string]bool, 0)
	writeListOfUrls(blank, path.Join(nasRoot(), "to-download.txt"))
}

func writeDownloads(urls map[string]bool) {
	writeListOfUrls(urls, path.Join(nasRoot(), "to-download.txt"))
}

func writeFailed(urls map[string]bool) {
	alreadyFailed := getContentsOfNasFile("failed-downloads.txt")
	// Add new failures to the list of already failed
	for url := range urls {
		alreadyFailed[url] = true
	}
	writeListOfUrls(alreadyFailed, path.Join(nasRoot(), "failed-downloads.txt"))
}

type dlresult struct {
	url string
	err error
}

func downloadEach(downloads map[string]bool) {
	failed := make(map[string]bool, 0)
	for url := range downloads {
		if strings.Contains(url, "youtube") || strings.Contains(url, "youtu.be") {
			err := downloadFromYoutube(url)
			if err != nil {
				fmt.Println(err)
				fmt.Fprintf(os.Stderr, "Failed to download `%v`: %v\n", url, err)
				failed[url] = true
			}
		}
	}
	if len(failed) > 0 {
		writeFailed(failed)
	}
	emptyDownloads()
}

func downloadFromYoutube(url string) error {
	dlDir := path.Join(nasRoot(), "refile")
	args := []string{
		"-f",
		"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
		"--no-playlist",
		"--merge-output-format",
		"mp4",
		url,
		"-o",
		"%(uploader)s/%(title)s.%(ext)s",
		"--restrict-filenames",
	}
	cmd := exec.Command("youtube-dl", args...)
	cmd.Dir = dlDir

	stdoutReader, err := cmd.StdoutPipe()
	if err != nil {
		return err
	}
	stdoutScanner := bufio.NewScanner(stdoutReader)

	split := func(data []byte, atEOF bool) (advance int, token []byte, err error) {
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
	stdoutScanner.Split(split)
	go func() {
		var title string
		for stdoutScanner.Scan() {
			text := stdoutScanner.Text()
			if strings.Contains(text, "Destination") {
				title = strings.TrimPrefix(text, "[download] Destination: ")
			}
			if strings.Contains(text, "ETA") {
				text = strings.TrimPrefix(text, "[download]")
				text = strings.TrimSpace(text)
				fmt.Printf("\r%v: %v%s", title, text, "          ")
			}
		}
		fmt.Println()
	}()

	err = cmd.Start()
	if err != nil {
		return fmt.Errorf("Couldn't start download: %v", err)
	}

	err = cmd.Wait()
	if err != nil {
		return fmt.Errorf("Couldn't complete download: %v", err)
	}
	return nil
}

func list(downloads map[string]bool) {
	for url := range downloads {
		fmt.Println(url)
	}
}

func add(downloads map[string]bool, url string) {
	reMarkdownURL := regexp.MustCompile(`\[.*\]\((.*)\)`)
	matches := reMarkdownURL.FindStringSubmatch(string(url))
	toAdd := ""
	if len(matches) > 0 {
		toAdd = matches[1]
	} else {
		toAdd = url
	}
	if _, ok := downloads[toAdd]; !ok {
		downloads[toAdd] = true
		fmt.Printf("Added `%v`\n", toAdd)
		writeDownloads(downloads)
	}

}
