package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"os"
	"os/exec"
	"path"
	"runtime"
	"sort"
	"strconv"
	"strings"
)

type Video struct {
	Title  string `json:"title"`
	Artist string `json:"artist"`
	URL    string `json:"url"`
}

func (v Video) String() string {
	return fmt.Sprintf("%s by %s", v.Title, v.Artist)
}

// readVideos reads a json file of video links
func readVideos() []Video {
	data := path.Join(os.Getenv("DATADIR"), "asmr.json")
	vidbytes, err := ioutil.ReadFile(data)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	var videos []Video
	err = json.Unmarshal(vidbytes, &videos)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	return videos
}

// writeVideos writes all videos to a json file
func writeVideos(videos []Video) {
	data, err := json.Marshal(videos)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	f, err := os.Create(path.Join(os.Getenv("DATADIR"), "asmr.json"))
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	defer f.Close()
	if _, err = f.Write(data); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

// openbrowser launches the url using the platform-specific method for URLs
func openbrowser(url string) {
	var err error

	switch runtime.GOOS {
	case "linux":
		err = exec.Command("xdg-open", url).Start()
	case "windows":
		err = exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
	case "darwin":
		err = exec.Command("open", url).Start()
	default:
		err = fmt.Errorf("unsupported platform")
	}
	if err != nil {
		log.Fatal(err)
	}

}

// checkForSimilarArtist will look if there is a similar artist already
// incase of typo when entering information.  Looks for Levenshtein distance
// of 2 or less
func checkForSimilarArtist(artists []string) string {
	var newArtist string
	fmt.Printf("Artist: ")
	fmt.Scanln(&newArtist)
	similar := make(map[string]bool, 0)
	exact := make(map[string]bool, 0)
	cache := make(map[string]int)
	for _, artist := range artists {
		dist, ok := cache[artist]
		if !ok {
			dist = levenshtein(newArtist, artist)
			cache[artist] = dist
		} else {
			fmt.Println("SKIPPING")
		}
		switch {
		case dist == 0:
			exact[artist] = true
		case dist < 3:
			similar[artist] = true
		default:
		}
	}
	if len(similar) > 0 && len(exact) == 0 {
		fmt.Println("Similar artists")
		i := 0
		similarArtists := make([]string, 0)
		for artist := range similar {
			fmt.Printf("\t%4d) %s\n", i, artist)
			i += 1
			similarArtists = append(similarArtists, artist)
		}
		fmt.Printf("Choose, or -1 to keep current: ")
		var choice int
		fmt.Scanln(&choice)
		if choice >= 0 {
			newArtist = similarArtists[choice]
		}
	}
	return newArtist
}

// urlify will convert to a proper url (incase of just youtube link added)
// update this to use a proper regex
func urlify(url string) string {
	if !strings.HasSuffix(url, "http") && !strings.HasSuffix(url, "www") {
		return fmt.Sprintf("https://www.youtube.com/watch?v=%s", url)
	}
	return url
}

// levenshtein calculates the levenshtein edit distance between two strings
func levenshtein(s, t string) int {
	d := make([][]int, len(s)+1)
	for i := range d {
		d[i] = make([]int, len(t)+1)
	}
	for i := range d {
		d[i][0] = i
	}
	for j := range d[0] {
		d[0][j] = j
	}
	for j := 1; j <= len(t); j++ {
		for i := 1; i <= len(s); i++ {
			if s[i-1] == t[j-1] {
				d[i][j] = d[i-1][j-1]
			} else {
				min := d[i-1][j]
				if d[i][j-1] < min {
					min = d[i][j-1]
				}
				if d[i-1][j-1] < min {
					min = d[i-1][j-1]
				}
				d[i][j] = min + 1
			}
		}

	}
	return d[len(s)][len(t)]
}

// delete removes all chosen videos
func delete(videos []Video, mask []int) []Video {
	var choices []int
	var response string
	fmt.Printf("Choice(s): ")
	fmt.Scanln(&response)
	for _, idx := range strings.Split(response, ",") {
		n, _ := strconv.ParseInt(idx, 10, 64)
		choices = append(choices, int(n))
	}
	sort.Reverse(sort.IntSlice(choices))
	for _, idx := range choices {
		videos = append(videos[:idx], videos[idx+1:]...)
	}
	return videos
}

// readChoices will take user input and split into ints
func readChoices() []int {
	var response string
	var choices []int
	fmt.Printf("Choice(s): ")
	fmt.Scanln(&response)
	for _, idx := range strings.Split(response, ",") {
		n, _ := strconv.ParseInt(idx, 10, 64)
		choices = append(choices, int(n))
	}
	return choices
}

// play opens all chosen videos (or a random one)
func play(videos []Video, mask []int, random bool) []Video {
	choices := []int{mask[rand.Intn(len(mask))]}
	if !random {
		choices = readChoices()
	}
	for _, idx := range choices {
		video := videos[idx]
		fmt.Printf("%s ~~ %s\n", video.Title, video.Artist)
		openbrowser(video.URL)
	}
	return videos
}

// add prompts for new video information
func add(videos []Video) []Video {
	newArtist := checkForSimilarArtist(getArtists(videos))
	var title, url string
	fmt.Printf("Title: ")
	fmt.Scanln(&title)
	fmt.Printf("URL: ")
	fmt.Scanln(&url)
	videos = append(videos, Video{title, newArtist, urlify(url)})
	return videos
}

func promptOrKeep(message, current string) string {
	fmt.Printf("%s (%s): ", message, current)
	var response string
	fmt.Scanln(&response)
	if response == "" {
		return current
	}
	return response
}

// modify will update the metadata on existing
func modify(videos []Video, mask []int) []Video {
	choices := readChoices()
	fmt.Println("Enter new values, or press enter to keep current")
	artists := getArtists(videos)
	for _, idx := range choices {
		videos[idx].Artist = checkForSimilarArtist(artists)
		videos[idx].Title = promptOrKeep("Title", videos[idx].Title)
		videos[idx].URL = promptOrKeep("URL", videos[idx].URL)
	}
	return videos
}

func getArtists(videos []Video) []string {
	artistMap := make(map[string]bool)
	for _, video := range videos {
		artistMap[video.Artist] = true
	}
	artists := make([]string, 0, len(artistMap))
	for artist, _ := range artistMap {
		artists = append(artists, artist)
	}
	return artists
}

func main() {
	videos := readVideos()
	cmd := os.Args[1]
	query := strings.ToLower(strings.Join(os.Args[2:], " "))

	mask := make([]int, 0)
	if cmd != "add" {
		fmt.Printf("    # %-20s %s\n", "ARTIST", "TITLE")
		fmt.Println(strings.Repeat("=", 60))
		for idx, video := range videos {
			artistMatches := strings.Contains(strings.ToLower(video.Artist), query)
			titleMatches := strings.Contains(strings.ToLower(video.Title), query)
			if artistMatches || titleMatches {
				fmt.Printf("%4d) %-20s %s\n", idx, video.Artist, video.Title)
				mask = append(mask, idx)
			}
		}
	}

	switch cmd {
	case "view": // Basically just a fallthrough as view happens by default
	case "play":
		play(videos, mask, false)
	case "add":
		videos = add(videos)
	case "delete":
		videos = delete(videos, mask)
	case "modify":
		videos = modify(videos, mask)
	default:
		fmt.Printf("Unrecognised command: %s\n", cmd)
	}
	writeVideos(videos)
}
