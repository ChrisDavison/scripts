package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
)

func main() {
	cmd := exec.Command("acpi")
	out, _ := cmd.Output()
	batStr := string(out)
	if strings.Contains(batStr, "Full") {
		fmt.Printf("B FULL\n")
		os.Exit(1)
	}
	parts := strings.Split(batStr, ", ")
	// status := parts[0]
	// pct := parts[1]
	rem := parts[2]
	remTime := strings.Split(rem, " ")[0][:5]
	arrowUp := "↑"
	arrowDown := "↓"
	arrow := arrowDown
	if strings.Contains(batStr, "Charging") {
		arrow = arrowUp
	}
	fmt.Printf("B%v %vh%v\n", arrow, remTime[:2], remTime[3:5])
}
