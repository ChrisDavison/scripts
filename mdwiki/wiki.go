package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"

	blackfriday "gopkg.in/russross/blackfriday.v2"
)

const viewTemplate = `<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/3.0.1/github-markdown.css">
<title>%s</title>
</head>

<body>
<a href="/">HOME</a>
<script>
    document.write('<a href="' + document.referrer + '">Go Back</a>');
</script>
<br>

<h1>%s</h1>
<div>%s</div>

</body>`

type page struct {
	title    string
	header   string
	contents []byte
}

func readMarkdownFileToHTML(filename string) ([]byte, error) {
	var body []byte
	var err error
	if !strings.HasSuffix(filename, ".md") {
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

	notesBody, err := readMarkdownFileToHTML("notes.md")
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
	fmt.Fprintf(w, viewTemplate, outputTitle, outputTitle, output)
	return
}

func dirHandler(w http.ResponseWriter, r *http.Request, direc string) {
	body, err := dirContentsAsLinks(direc)
	if err != nil {
		log.Println(err)
		return
	}
	title := filenameToTitle(r.URL.Path[1:])
	fmt.Fprintf(w, viewTemplate, title, title, body)
	return
}

func fileHandler(w http.ResponseWriter, r *http.Request, file string) {
	if !strings.HasSuffix(file, ".md") {
		http.ServeFile(w, r, file)
		return
	}
	body, err := readMarkdownFileToHTML(file)
	if err != nil {
		http.Redirect(w, r, "/edit/"+r.URL.Path[1:], http.StatusFound)
		return
	}
	title := filenameToTitle(r.URL.Path[1:])
	fmt.Fprintf(w, viewTemplate, title, title, body)
}

func viewHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("GET", r.URL.Path)
	if r.URL.Path == "/" {
		rootHandler(w, r)
		return
	}
	stat, err := os.Stat(r.URL.Path[1:])
	if err != nil {
		log.Println(r.URL.Path[1:], err)
		return
	}
	if stat.IsDir() {
		dirHandler(w, r, r.URL.Path[1:])
	} else {
		fileHandler(w, r, r.URL.Path[1:])
	}
}

func filenameToTitle(filename string) string {
	noExt := strings.TrimSuffix(filename, ".md")
	title := strings.Title(strings.Replace(noExt, "-", " ", -1))
	return title
}

func filenameAsListAhref(filename, dir string) string {
	joined := strings.Join([]string{"", dir, filename}, "/")
	return fmt.Sprintf(`<li><a href="%s">%s</a></li>`, joined, filenameToTitle(filename))
}

func getSubdirsAndFilesInDir(contents []os.FileInfo, withDotfiles bool) ([]os.FileInfo, []os.FileInfo) {
	var dirs []os.FileInfo
	var files []os.FileInfo

	for _, fileinfo := range contents {
		if strings.HasPrefix(fileinfo.Name(), ".") && !withDotfiles {
			continue
		}
		if fileinfo.IsDir() {
			dirs = append(dirs, fileinfo)
		} else {
			files = append(files, fileinfo)
		}
	}
	return dirs, files
}

func dirContentsAsLinks(dir string) ([]byte, error) {
	contents, err := ioutil.ReadDir(dir)
	if err != nil {
		log.Println("Err reading dir:", err)
		return nil, err
	}

	dirs, files := getSubdirsAndFilesInDir(contents, false)
	output := ""
	if dirs != nil {
		output += "<h2>Dirs</h2><ul>"
		for _, subdir := range dirs {
			output += filenameAsListAhref(subdir.Name(), dir)
		}
		output += "</ul>"
	}
	if files != nil {
		output += "<h2>Notes</h2><ul>"
		for _, file := range files {
			output += filenameAsListAhref(file.Name(), dir)
		}
		output += "</ul>"
	}

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
