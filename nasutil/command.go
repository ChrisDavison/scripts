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
	urls map[string]bool
}

func (d *DownloadList) summary() {
	n_failed, n_to_download := 0, 0
	for _, failed := range d.urls {
		if failed {
			n_failed += 1
		} else {
			n_to_download += 1
		}
	}
	fmt.Printf("%d URLs to download. %d previously failed.\n", n_to_download, n_failed)
}

func (d *DownloadList) list() {
	for url, failed := range d.urls {
		if !failed {
			fmt.Println(url)
		}
	}
}

func (d *DownloadList) listFailed() {
	for url, failed := range d.urls {
		if failed {
			fmt.Println(url)
		}
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
		d.urls[toAdd] = false
		fmt.Printf("Added `%v`\n", toAdd)
	}
}

func (d *DownloadList) downloadEach() {
	for url, failed := range d.urls {
		if failed {
			continue
		}
		if strings.Contains(url, "youtube") || strings.Contains(url, "youtu.be") {
			err := downloadFromYoutube(url)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Failed to download `%v`: %v\n", url, err)
				d.urls[url] = true
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

	err = cmd.Wait()
	if err != nil {
		return fmt.Errorf("couldn't complete download: %v", err)
	}
	return nil
}

func (d *DownloadList) Save() {
	writeListOfUrls(d.urls, path.Join(nasRoot(), fnDownloads))
}

func (d *DownloadList) EmptyDownloads() {
	blank := make(map[string]bool)
	d.urls = blank
}

func (d *DownloadList) EmptyFailures() {
	newUrls := make(map[string]bool)
	for url, failed := range d.urls {
		if !failed {
			newUrls[url] = false
		}
	}
	d.urls = newUrls
}

func GetDownloadList() DownloadList {
	f, err := os.Open(path.Join(nasRoot(), fnDownloads))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Couldn't open `%v`: %v\n", fnDownloads, err)
		os.Exit(ERR_COULDNT_OPEN_FILE)
	}
	defer f.Close()
	bufreader := bufio.NewScanner(f)
	lines := make(map[string]bool)
	for bufreader.Scan() {
		line := bufreader.Text()
		parts := strings.Split(line, " ")
		url := line
		failed := false
		if len(parts) > 1 {
			url = strings.Join(parts[:len(parts)-1], " ")
			failed = parts[len(parts)-1] == "FAILED"
		}
		if didfail, exists := lines[url]; exists {
			lines[url] = didfail || failed
		} else {
			lines[url] = failed
		}
	}
	return DownloadList{lines}
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
	for url, failed := range urls {
		msg := url
		if failed {
			msg += " FAILED"
		}
		_, err := fbuf.WriteString(msg + "\n")
		if err != nil {
			fmt.Fprintf(os.Stderr, "Couldn't write url `%v` to file: %v", url, err)
			os.Exit(ERR_COULDNT_WRITE_FILE)
		}
	}
}
