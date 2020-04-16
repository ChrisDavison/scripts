package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"path"
	"regexp"
	"sort"
	"strings"
)

var (
	count    = flag.Bool("count", false, "Count of links per file")
	orphaned = flag.Bool("orphaned", false, "Files that are not linked to")
	forward  = flag.Bool("forward", false, "Show links FROM files instead")
)

// linksInFile reads a file and returns a list of filename links
// where a 'filename' link is a link to something with .md extension
func linksInFile(filename string) []string {
	rx := regexp.MustCompile(`\((?:\./)*([a-zA-Z0-9\-_]*?\.md)\)`)
	contentsBytes, err := ioutil.ReadFile(filename)
	contents := string(contentsBytes)
	if err != nil {
		log.Printf("Read file: %s\n", filename)
	}
	links := make([]string, 0, 100)
	for _, match := range rx.FindAllStringSubmatch(contents, -1) {
		links = append(links, strings.ToLower(match[1]))
	}
	return links
}

// getBacklinks finds file links in every md file under current dir
// and returns a map of: filename to []string{files linking to filename}
func getBacklinks() map[string][]string {
	backlinks := make(map[string][]string)
	fileinfos, err := ioutil.ReadDir(".")
	if err != nil {
		log.Fatal("Reading dir for backlinks")
	}
	for _, fileinfo := range fileinfos {
		if fileinfo.IsDir() || !(path.Ext(fileinfo.Name()) == ".md") {
			continue
		}
		links := linksInFile(fileinfo.Name())
		for _, filename := range links {
			fn_lower := strings.ToLower(filename)
			backlinks[fn_lower] = append(backlinks[fn_lower], fileinfo.Name())
		}
	}
	return backlinks
}

// printCountedForwardLinks displays file links for each of `files`
func printCountedForwardLinks(files []string) {
	type fileAndLinks struct {
		filename  string
		linkcount uint
	}
	filelinks := make([]fileAndLinks, 0, len(files))
	for _, filename := range files {
		links := linksInFile(filename)
		if len(links) == 0 {
			continue
		}
		filelinks = append(filelinks, fileAndLinks{filename, uint(len(links))})
	}
	sort.Slice(filelinks, func(i, j int) bool {
		return filelinks[i].linkcount > filelinks[j].linkcount
	})
	for _, entry := range filelinks {
		fmt.Printf("%5d %s\n", entry.linkcount, entry.filename)
	}
}

// printForwardLinks displays file links for each of `files`
func printForwardLinks(files []string) {
	for _, filename := range files {
		links := linksInFile(filename)
		if len(links) == 0 {
			continue
		}
		fmt.Println(filename)
		for _, link := range links {
			fmt.Printf(" > %s\n", link)
		}
	}
}

// printBacklinks displays all other files that link TO each of `files`
func printBacklinks(files []string) {
	backlinks := getBacklinks()
	for _, filename := range files {
		links, ok := backlinks[strings.ToLower(filename)]
		if !ok {
			continue
		}
		fmt.Println(filename)
		for _, link := range links {
			fmt.Printf(" ^ %s\n", link)
		}
	}
}

// printCountedBacklinks shows how many other files links to each of `files`
func printCountedBacklinks(files []string) {
	backlinks := getBacklinks()
	type linksForFile struct {
		filename string
		links    []string
	}
	filesAndLinks := make([]linksForFile, 0, len(backlinks))
	for filename, links := range backlinks {
		if len(links) == 0 {
			continue
		}

		filesAndLinks = append(filesAndLinks, linksForFile{
			filename,
			links,
		})
	}
	sort.Slice(filesAndLinks, func(i, j int) bool {
		return len(filesAndLinks[i].links) > len(filesAndLinks[j].links)
	})
	for _, filenameLinks := range filesAndLinks {
		fmt.Printf("%5d %s\n", len(filenameLinks.links), filenameLinks.filename)
	}
}

// printOrpans displays all files that no other file links to
// optionally filtered to only show if each passed file is linked to.
func printOrphans(files []string) {
	backlinks := getBacklinks()
	for _, file := range files {
		if _, ok := backlinks[file]; !ok {
			fmt.Println(file)
		}
	}
}

// getFilesFromGlob will return all .md files under the current directory, sorted
func getFilesFromGlob() []string {
	files := make([]string, 0, 100)
	fileinfos, err := ioutil.ReadDir(".")
	if err != nil {
		log.Fatal(err)
	}
	for _, fileinfo := range fileinfos {
		if fileinfo.IsDir() || !strings.HasSuffix(fileinfo.Name(), ".md") {
			continue
		}
		files = append(files, fileinfo.Name())
	}
	sort.Strings(files)

	return files
}

func main() {
	flag.Parse()
	files := flag.Args()
	if len(files) == 0 {
		files = getFilesFromGlob()
	}
	if *orphaned {
		printOrphans(files)
	} else if *forward {
		if *count {
			printCountedForwardLinks(files)
		} else {
			printForwardLinks(files)
		}
	} else {
		if *count {
			printCountedBacklinks(files)
		} else {
			printBacklinks(files)
		}
	}
	fmt.Println("---")
}
