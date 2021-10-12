package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"strconv"
	"strings"
)

const USAGE string = `usage: laptop-brightness up|down|current

Increase or decrease screen brightness, at hardware level, by 5% of max.
Values limited to 0..MAX_BRIGHTNESS

up | down -> increase or decrease by 5%
current   -> display current brightness as %max

This script needs root access. You CAN use sudo, but to use without a password
prompt,

# Append to /etc/sudoers...
Cmnd_Alias BRIGHT_CMDS=/PATH/TO/THIS/COMPILED up, /PATH/TO/THIS/COMPILED down
username ALL=(root) NOPASSWD: BRIGHT_CMDS
`

const DEVICE_DIR string = "/sys/class/backlight/intel_backlight"

const (
	ERR_READ_BRIGHTNESS = iota + 1
	ERR_WRITE
	ERR_CLI_ARGS
	ERR_NO_HARDWARE
)

type Brightness struct {
	current int64
	max     int64
	step    int64
}

func parseIntFromFile(path string) (int64, error) {
	brightness, err := ioutil.ReadFile(path)
	if err != nil {
		return 0, err
	}
	brightnessVal, err := strconv.ParseInt(strings.TrimSpace(string(brightness)), 10, 64)
	if err != nil {
		return 0, err
	}
	return brightnessVal, nil
}

func NewBrightness() *Brightness {
	if _, err := os.Stat(DEVICE_DIR); os.IsNotExist(err) {
		fmt.Fprintf(os.Stderr, "No backlight hardware listed in /sys/class/backlight: %s\n", err)
		os.Exit(ERR_NO_HARDWARE)
	}

	currentBrightness, err := parseIntFromFile(path.Join(DEVICE_DIR, "brightness"))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Couldn't read current brightness: %s", err)
		os.Exit(ERR_READ_BRIGHTNESS)
	}

	maxBrightness, err := parseIntFromFile(path.Join(DEVICE_DIR, "max_brightness"))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Couldn't read max brightness: %s", err)
		os.Exit(ERR_READ_BRIGHTNESS)
	}

	return &Brightness{
		currentBrightness,
		maxBrightness,
		maxBrightness / 20,
	}
}

func (b *Brightness) Increase() {
	b.current += b.step
	if b.current > b.max {
		b.current = b.max
	}
}

func (b *Brightness) Decrease() {
	b.current -= b.step
	if b.current < 0 {
		b.current = 0
	}
}

func (b *Brightness) WriteToFile() {
	brightnessPath := path.Join(DEVICE_DIR, "brightness")
	f, err := os.Create(brightnessPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Couldn't write brightness: %v", err)
		os.Exit(ERR_WRITE)
	}
	defer f.Close()
	fmt.Fprintln(f, b.current)
}

func (b *Brightness) CurrentPercent() float64 {
	return float64(b.current) / float64(b.max) * 100
}

func main() {
	if len(os.Args) == 1 {
		fmt.Println(USAGE)
		os.Exit(0)
	}
	operation := os.Args[1]
	brightness := NewBrightness()
	if operation == "current" {
		fmt.Printf("%v", brightness.CurrentPercent())
		return
	} else if operation == "up" {
		brightness.Increase()
		brightness.WriteToFile()
	} else if operation == "down" {
		brightness.Decrease()
		brightness.WriteToFile()
	} else {
		fmt.Fprintf(os.Stderr, "Argument $1 must be either 'up', 'down', or 'current'.")
		os.Exit(ERR_CLI_ARGS)
	}
}
