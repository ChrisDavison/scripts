package main

import "testing"

func TestFilterJunk(t *testing.T) {
	testcases := []struct {
		input []string
		want  []string
	}{
		{
			[]string{"this", "is", "a", "string"},
			[]string{"this", "string"},
		},
	}
	for _, tc := range testcases {
		got := filterJunk(tc.input)
		for i := range tc.want {
			if got[i] != tc.want[i] {
				t.Errorf("Got: %s, want: %s\n", got, tc.want)
			}
		}
	}
}

func TestEmptySimilarityString(t *testing.T) {
	testcases := []struct {
		input SimilarityPair
		want  string
	}{
		{SimilarityPair{"", "", 0}, "0.00 ::  - "},
	}
	for _, tc := range testcases {
		got := tc.input.String()
		if got != tc.want {
			t.Errorf("Got: %s, want: %s\n", got, tc.want)
		}
	}
}

func TestSimilarityString(t *testing.T) {
	testcases := []struct {
		input SimilarityPair
		want  string
	}{
		{SimilarityPair{"String", "String", 1}, "1.00 :: String - String"},
	}
	for _, tc := range testcases {
		got := tc.input.String()
		if got != tc.want {
			t.Errorf("Got: %s, want: %s\n", got, tc.want)
		}
	}
}
