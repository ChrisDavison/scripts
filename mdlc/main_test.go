package main

import "testing"

func TestIsLocalLink(t *testing.T) {
	inputs := []struct {
		input string
		want  bool
	}{
		{"www.google.com", false},
		{"http://www.google.com", false},
		{"https://www.google.com", false},
		{"./local.md", true},
	}
	for _, set := range inputs {
		got := isLocalLink(set.input)
		if got != set.want {
			t.Errorf("%s\n\tGot: %v\n\tWant: %v\n", set.input, got, set.want)
		}
	}
}

func TestLinksInLine(t *testing.T) {
	inputs := []struct {
		input string
		want  []string
	}{
		{"Some text [link](www.google.com)", []string{"www.google.com"}},
	}
	for _, set := range inputs {
		got := linksInLine(set.input)
		if got != set.want {
			t.Errorf("%s\n\tGot: %v\n\tWant: %v\n", set.input, got, set.want)
		}
	}
}
