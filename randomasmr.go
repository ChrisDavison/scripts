// randomasmr.go

package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os/user"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

func expand(path string) (string, error) {
	if len(path) == 0 || path[0] != '~' {
		return path, nil
	}

	usr, err := user.Current()
	if err != nil {
		return "", err
	}
	return filepath.Join(usr.HomeDir, path[1:]), nil
}

func main() {
	tokenpath, err := expand("~/.pinboard")
	if err != nil {
		log.Fatal(err)
	}
	pinboardToken, err := ioutil.ReadFile(tokenpath)
	if err != nil {
		log.Fatal(err)
	}

	pinboardAPIURL := "https://api.pinboard.in/v1/posts/all?tag=asmr"
	pinboardURL := fmt.Sprintf("%s&auth_token=%s", pinboardAPIURL, strings.TrimSpace(string(pinboardToken)))
	resp, err := http.Get(pinboardURL)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
	}
	re := regexp.MustCompile(`href="(.*?)"\s`)
	matches := re.FindAllStringSubmatch(string(body), -1)
	if matches != nil {
		rand.Seed(time.Now().UnixNano())
		randint := rand.Int() % len(matches)
		fmt.Println(matches[randint][1])
	}
}
