package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"path"
	"regexp"
	"strings"
)

const (
	fnDownloads = "to-download.txt"
	fnFailed    = "failed-downloads.txt"
)

type DownloadList struct {
	urls     map[string]bool
	failures map[string]bool
}

func (d *DownloadList) summary() {
	fmt.Printf("%d URLs to download. %d previously failed.\n", len(d.urls), len(d.failures))
}

func (d *DownloadList) list() {
	for url := range d.urls {
		fmt.Println(url)
	}
}

func (d *DownloadList) listFailed() {
	for url := range d.failures {
		fmt.Println(url)
	}
}

func (d *DownloadList) add(url string) {
	reMarkdownURL := regexp.MustCompile(`\[.*\]\((.*)\)`)
	matches := reMarkdownURL.FindStringSubmatch(string(url))
	toAdd := ""
	if len(matches) > 0 {
		toAdd = matches[1]
	} else {
		toAdd = strings.Split(url, "&")[0]
	}
	if _, ok := d.urls[toAdd]; !ok {
		d.urls[toAdd] = true
		fmt.Printf("Added `%v`\n", toAdd)
	}
}

func (d *DownloadList) downloadEach() {
	for url := range d.urls {
		if strings.Contains(url, "youtube") || strings.Contains(url, "youtu.be") {
			err := downloadFromYoutube(url)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Failed to download `%v`: %v\n", url, err)
				d.failures[url] = true
			}
		}
	}
	d.urls = make(map[string]bool)
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
	// cmd := exec.Command("youtube-dl", args...)
	cmd := exec.Command("yt-dlp", args...)
	cmd.Dir = dlDir

	stdoutReader, err := cmd.StdoutPipe()
	if err != nil {
		return err
	}
	stdoutScanner := bufio.NewScanner(stdoutReader)
	stdoutScanner.Split(splitEitherCRLF)

	// Scan the stdout of the download
	// Capture the video name, and only print download speed
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
				fmt.Printf("\r%v: %v        ", title, text)
			}
		}
		fmt.Println()
	}()

	err = cmd.Start()
	if err != nil {
		return fmt.Errorf("couldn't start download: %v", err)
	}
	// }

	err = cmd.Wait()
	if err != nil {
		return fmt.Errorf("couldn't complete download: %v", err)
	}
	return nil
}

func (d *DownloadList) SaveFiles() {
	writeListOfUrls(d.urls, path.Join(nasRoot(), fnDownloads))
	writeListOfUrls(d.failures, path.Join(nasRoot(), fnFailed))
}

func (d *DownloadList) EmptyDownloads() {
	blank := make(map[string]bool)
	writeListOfUrls(blank, path.Join(nasRoot(), fnDownloads))
}

func (d *DownloadList) EmptyFailures() {
	blank := make(map[string]bool)
	writeListOfUrls(blank, path.Join(nasRoot(), fnFailed))
}

func GetDownloadList() DownloadList {
	return DownloadList{
		getContentsOfNasFile(fnDownloads),
		getContentsOfNasFile(fnFailed),
	}
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
	lines := make(map[string]bool)
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
