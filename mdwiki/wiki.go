package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	blackfriday "gopkg.in/russross/blackfriday.v2"
)

type page struct {
	title    string
	header   string
	contents []byte
}

func readMarkdownFileToHTML(filename string) ([]byte, error) {
	var body []byte
	var err error
	if !strings.HasSuffix(filename, ".txt") && !strings.HasSuffix(filename, ".md") {
		filename = filename + ".md"
	}
	body, err = ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Reading Markdown :: %v: %v\n", filename, err)
		return nil, err
	}
	return blackfriday.Run(body), err
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	outputTitle := "Notes.md & Files in Root"
	output := []byte{}

	notesBody, err := readMarkdownFileToHTML("inbox.txt")
	if err != nil {
		// http.Redirect(w, r, "/edit/notes", http.StatusFound)
		return
	}
	output = append(output, notesBody...)

	body, err := dirContentsAsLinks(".")
	if err != nil {
		log.Println(err)
		return
	}
	output = append(output, body...)
	fmt.Fprintf(w, VIEW_TEMPLATE, outputTitle, outputTitle, output)
	return
}

func dirHandler(w http.ResponseWriter, r *http.Request, direc string) {
	body, err := dirContentsAsLinks(direc)
	if err != nil {
		log.Println(err)
		return
	}
	title := filenameToTitle(r.URL.Path[1:])
	fmt.Fprintf(w, VIEW_TEMPLATE, title, title, body)
	return
}

func fileHandler(w http.ResponseWriter, r *http.Request, file string) {
	if !strings.HasSuffix(file, ".txt") && !strings.HasSuffix(file, ".md") {
		http.ServeFile(w, r, file)
		return
	}
	body, err := readMarkdownFileToHTML(file)
	if err != nil {
		http.Redirect(w, r, "/edit/"+r.URL.Path[1:], http.StatusFound)
		return
	}
	title := filenameToTitle(r.URL.Path[1:])
	fmt.Fprintf(w, VIEW_TEMPLATE, title, title, body)
}

func filenameToTitle(filename string) string {
	noExt := strings.TrimSuffix(filename, filepath.Ext(filename))
	title := strings.Title(strings.Replace(noExt, "-", " ", -1))
	return title
}

func filenameAsListAhref(filename, dir string) string {
	joined := strings.Join([]string{"", dir, filename}, "/")
	return fmt.Sprintf(`<li><a href="%s">%s</a></li>`, joined, filenameToTitle(filename))
}

func dirContentsAsLinks(dir string) ([]byte, error) {
	contents, err := ioutil.ReadDir(dir)
	if err != nil {
		log.Println("Err reading dir:", err)
		return nil, err
	}

	withDotfiles := false
	dirString, fileString := "", ""
	for _, fileinfo := range contents {
		if strings.HasPrefix(fileinfo.Name(), ".") && !withDotfiles {
			continue
		}
		if fileinfo.IsDir() {
			dirString += filenameAsListAhref(fileinfo.Name(), dir)
		} else {
			fileString += filenameAsListAhref(fileinfo.Name(), dir)
		}
	}

	output := fmt.Sprintf(DIR_CONTENTS_TEMPLATE, dirString, fileString)

	return []byte(output), nil
}

func main() {
	if len(os.Args) > 1 {
		os.Chdir(os.Args[1])
	}

	http.HandleFunc("/", viewHandler)
	log.Println("Registered handler `viewHandler` to `/`")
	// http.HandleFunc("/edit/", editHandler)
	// http.HandleFunc("/save/", saveHandler)
	log.Println("Listening on 8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
