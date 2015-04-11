package main

import (
	"fmt"
	"flag"
	"bytes"
	"os/exec"
	"log"
)

var doi = flag.String("doi", "", "DOI to convert to Bibtex")
var tgt = flag.String("fn", "", "Bib filename (append)")

func main(){
	flag.Parse()
	header := "Accept: text/bibliography; style=bibtex"
	command := "curl -LH"
	urlBase := "http://dx.doi.org/"

	if *doi == ""{
		flag.Usage()
		return
	}
	out := fmt.Sprintf("%v \"%v\" %v%v", command, header, urlBase, *doi)

	cmd := exec.Command("sh", "-c", out)
	var bufOut bytes.Buffer
	cmd.Stdout = &bufOut

	err := cmd.Run()
	if err != nil{
		log.Fatal(err)
	}

	fmt.Printf("%v", bufOut.String())
}
