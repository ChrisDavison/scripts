package main

import (
	"fmt"
	"os"
	"strconv"
)

const USAGE = `latlong_to_ddd - convert degrees-minutes-seconds to decimal-degrees

usage:
	latlong_to_ddd [-s -w] D_north M_north S_north D_east M_east S_east

options:
	-s    First degree-minutes-seconds is actually South
	-w    Second degree-minutes-seconds is actually West
`

func toDecimalDegrees(degrees, minutes, seconds float64) float64 {
	minPlusSec := (minutes + (seconds / 60))
	return degrees + (minPlusSec / 60)
}

func main() {
	args := make([]float64, 0)
	isSouth := false
	isWest := false

	for _, arg := range os.Args[1:] {
		if arg == "-s" {
			isSouth = true
		} else if arg == "-w" {
			isWest = true
		} else {
			val, err := strconv.ParseFloat(arg, 10)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error parsing `%s`: %s\n", arg, err)
				os.Exit(1)
			}
			args = append(args, val)
		}
	}
	if len(args) != 6 {
		fmt.Fprintln(os.Stderr, "Not enough args.")
		fmt.Println(USAGE)
		os.Exit(2)
	}
	d_north, m_north, s_north, d_east, m_east, s_east := args[0], args[1], args[2], args[3], args[4], args[5]

	ddd_north := toDecimalDegrees(d_north, m_north, s_north)
	ddd_east := toDecimalDegrees(d_east, m_east, s_east)
	if isSouth {
		ddd_north *= -1
	}
	if isWest {
		ddd_east *= -1
	}
	fmt.Printf("%f,%f\n", ddd_north, ddd_east)
}
