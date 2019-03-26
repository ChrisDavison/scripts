package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"strings"
)

const version = "0.2.0"

func main() {
	if len(os.Args) > 1 && os.Args[1] == "version" {
		fmt.Println("git-branchstat", version)
		return
	}
	if !isGitRepo() {
		log.Fatal("Not a git repo")
	}
	outputs := make([]string, 0, 4)
	if ab := getAheadBehind(); ab != "" {
		outputs = append(outputs, ab)
	}
	if mod := getModified(); mod != "" {
		outputs = append(outputs, mod)
	}
	if stat := getStatus(); stat != "" {
		outputs = append(outputs, stat)
	}
	if untracked := getUntracked(); untracked != "" {
		outputs = append(outputs, untracked)
	}
	fmt.Println(strings.Join(outputs, ", "))
}

func getAheadBehind() string {
	args := []string{
		"for-each-ref",
		"--format='%(refname:short) %(upstream:track)'",
		"refs/heads",
	}
	out, err := gitOutput(args)
	if err != nil {
		log.Fatalf("%s\n", err)
	}
	changedBranches := []string{}
	for _, line := range strings.Split(out, "\n") {
		tidied := strings.Trim(line, "'\" ")
		if len(strings.Split(tidied, " ")) > 1 {
			changedBranches = append(changedBranches, tidied)
		}
	}
	return strings.Join(changedBranches, ", ")
}

func getModified() string {
	out, err := gitOutput([]string{"diff", "--stat"})
	if err != nil {
		log.Fatal(err)
	}
	nmodified := strings.Count(strings.TrimRight(out, "\n"), "\n")
	msg := ""
	if nmodified > 0 {
		msg = fmt.Sprintf("Modified %d", nmodified)
	}
	return msg
}

func getStatus() string {
	out, err := gitOutput([]string{"diff", "--stat", "--cached"})
	if err != nil {
		log.Fatal(err)
	}
	nstaged := strings.Count(out, "\n")
	msg := ""
	if nstaged > 0 {
		msg = fmt.Sprintf("Staged %d", nstaged)
	}
	return msg
}

func getUntracked() string {
	out, err := gitOutput([]string{"ls-files", "--others", "--exclude-standard"})
	if err != nil {
		log.Fatal(err)
	}
	nuntracked := strings.Count(out, "\n")
	msg := ""
	if nuntracked > 0 {
		msg = fmt.Sprintf("Untracked %d", nuntracked)
	}
	return msg
}

func gitOutput(args []string) (string, error) {
	cmdEditor := exec.Command("git", args...)
	out, err := cmdEditor.Output()
	if err != nil {
		return "", err
	}
	return string(out[:]), nil
}

func isGitRepo() bool {
	contents, err := ioutil.ReadDir(".")
	if err != nil {
		log.Fatalf("Error checking if git repo: %s\n", err)
	}
	for _, fp := range contents {
		if fp.IsDir() && fp.Name() == ".git" {
			return true
		}
	}
	return false
}
