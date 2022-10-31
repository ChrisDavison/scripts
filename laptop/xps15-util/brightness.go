package main

import (
	"fmt"
	"os"
	"strings"
)

const brightnessFile string = "/sys/class/backlight/intel_backlight/brightness"
const maxBrightnessFile string = "/sys/class/backlight/intel_backlight/max_brightness"

func brightnessHelp() {
	fmt.Println("xps15-util brightness show|increase|decrease")
	os.Exit(1)
}

func getCurrentBrightness() int64 {
	val, err := readIntFromFile(brightnessFile)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error getting current brightness: %s\n", err)
		os.Exit(1)
	}
	return val
}

func getMaxBrightness() int64 {
	val, err := readIntFromFile(maxBrightnessFile)
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
		newBrightness += step
		if newBrightness > maxBrightness {
			newBrightness = maxBrightness
		}
	} else {
		newBrightness -= step
		if newBrightness < 0 {
			newBrightness = 0
		}
	}
	err := os.WriteFile(brightnessFile, []byte(fmt.Sprintf("%d", newBrightness)), 0644)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(3)
	}
}

func showBrightness() {
	pct := float64(getCurrentBrightness()) / float64(getMaxBrightness()) * 100
	fmt.Printf("Brightness: %.0f%%\n", pct)
}

func brightness(args []string) {
	bCmd := "help"
	if len(args) > 0 {
		bCmd = strings.ToLower(string(args[0]))
	}
	if inList(bCmd, []string{"show", "s", "--show"}) {
		showBrightness()
	} else if inList(bCmd, []string{"up", "increase", "--up", "u"}) {
		changeBrightness(true)
	} else if inList(bCmd, []string{"down", "d", "--down", "decrease"}) {
		changeBrightness(false)
	} else {
		brightnessHelp()
	}
}
