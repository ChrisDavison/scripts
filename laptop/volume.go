package main

import (
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

func activeSink() string {
	out, err := exec.Command("pactl", "list", "short", "sinks").Output()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	for _, line := range out {
		line := string(line)
		if strings.Contains(line, "RUNNING") && !strings.Contains(line, "Pulse") {
			parts := strings.Split(line, " ")
			return parts[2]
		}
	}
	return ""
}

func muteVolume() {
	cmd := exec.Command("pactl", "set-sink-mute", activeSink(), "toggle")
	cmd.Run()
}

func currentVolume() int64 {
	out, err := exec.Command("pactl", "list", "sinks").Output()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(3)
	}
	start := false
	startLine := "Name: " + activeSink()
	volume := int64(0)
	for _, line := range out {
		line := string(line)
		if strings.Contains(line, startLine) {
			start = true
		}
		if start && strings.Contains(line, "Volume") {
			val, err := strconv.ParseInt(line, 64, 10)
			if err != nil {
				fmt.Fprintln(os.Stderr, err)
				os.Exit(4)
			}
			volume = val
		}
		// TODO
	}
	return volume
}

func changeVolume(increase bool) {
	sign := ""
	if !increase {
		sign = "-"
	}
	cmd := exec.Command("pactl", "set-sink-volume", activeSink(), sign+"3dB")
	cmd.Run()
}
func showVolume() {}

func volume(args []string) {
	vCmd := strings.ToLower(string(args[0]))
	if inList(vCmd, []string{"show", "s", "--show"}) {
		showVolume()
	} else if inList(vCmd, []string{"up", "increase", "--up", "u"}) {
		changeVolume(true)
	} else if inList(vCmd, []string{"down", "d", "--down", "decrease"}) {
		changeVolume(false)
	} else if inList(vCmd, []string{"mute", "m", "--mute", "silence", "silent"}) {
		muteVolume()
	} else {
		help()
	}
}
