package main

import (
	"fmt"
	"os"
	"strings"
)

func getCurrentBrightness() int64 {
	val, err := readIntFromFile("/sys/class/backlight/brightness")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error getting current brightness: %s\n", err)
		os.Exit(1)
	}
	return val
}

func getMaxBrightness() int64 {
	val, err := readIntFromFile("/sys/class/backlight/brightness")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error getting current brightness: %s\n", err)
		os.Exit(1)
	}
	return val
}

func changeBrightness(increase bool) {
	newBrightness := getCurrentBrightness()
	maxBrightness := getMaxBrightness()
	step := maxBrightness / 20
	if increase {
		newBrightness += newBrightness + step
		if newBrightness > maxBrightness {
			newBrightness = maxBrightness
		}
	} else {
		newBrightness -= step
		if newBrightness < 0 {
			newBrightness = 0
		}
	}
}

func showBrightness() {
	pct := float64(getCurrentBrightness()/getMaxBrightness()) * 100
	fmt.Printf("Brightness: %.2f %%\n", pct)
}
func brightness(args []string) {
	bCmd := strings.ToLower(string(args[0]))
	if inList(bCmd, []string{"show", "s", "--show"}) {
		showBrightness()
	} else if inList(bCmd, []string{"up", "increase", "--up", "u"}) {
		changeBrightness(true)
	} else if inList(bCmd, []string{"down", "d", "--down", "decrease"}) {
		changeBrightness(false)
	} else {
		help()
	}
}
