package main

import (
	"log"
	"net/http"
	"os"
)

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
