package main

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

const volumeHelpStr string = `xps15-util volume up|down|show|mute`

func volumeHelp() {
	fmt.Println(volumeHelpStr)
	os.Exit(1)
}

func activeSink() string {
	out, err := exec.Command("pactl", "list", "short", "sinks").Output()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	for _, line := range bytes.Split(out, []byte{'\n'}) {
		line := string(line)
		if strings.Contains(line, "RUNNING") && !strings.Contains(line, "Pulse") {
			parts := strings.Split(line, "\t")
			return parts[1]
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
	for _, line := range bytes.Split(out, []byte{'\n'}) {
		line := string(line)
		if strings.Contains(line, startLine) {
			start = true
		}
		if start && strings.Contains(line, "Volume") {
			if strings.HasPrefix(line, "Sink") || strings.Contains(line, "Base Volume") {
				return volume
			}
			parts := strings.Split(line, "dB")
			partsSplit := strings.Split(strings.TrimSpace(parts[0]), " ")
			db := partsSplit[len(partsSplit)-1]
			val, err := strconv.ParseInt(strings.Split(db, ".")[0], 10, 64)
			if err != nil {
				fmt.Fprintln(os.Stderr, err)
				os.Exit(4)
			}
			volume = val
		}
	}
	return volume
}

func changeVolume(increase bool) {
	sign := "+"
	if !increase {
		sign = "-"
	}
	cmd := exec.Command("pactl", "set-sink-volume", activeSink(), sign+"3dB")
	cmd.Run()
}

func showVolume() {
	fmt.Printf("Volume: %vdB\n", currentVolume())
}

func volume(args []string) {
	vCmd := ""
	if len(args) > 0 {
		vCmd = strings.ToLower(string(args[0]))
	}
	if inList(vCmd, []string{"show", "s", "--show"}) {
		showVolume()
	} else if inList(vCmd, []string{"up", "increase", "--up", "u"}) {
		changeVolume(true)
	} else if inList(vCmd, []string{"down", "d", "--down", "decrease"}) {
		changeVolume(false)
	} else if inList(vCmd, []string{"mute", "m", "--mute", "silence", "silent"}) {
		muteVolume()
	} else {
		volumeHelp()
	}
}
