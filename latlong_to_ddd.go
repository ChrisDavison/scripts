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

type config struct {
	isSouth bool
	isWest  bool
	args    []float64
}

func parseArgs(args []string) (c config, err error) {
	isSouth, isWest := false, false
	latlongArgs := []float64{}
	for _, arg := range args {
		switch arg {
		case "-s":
			isSouth = true
		case "-w":
			isWest = true
		default:
			val, err := strconv.ParseFloat(arg, 10)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error parsing `%s`: %s\n", arg, err)
				os.Exit(1)
			}
			latlongArgs = append(latlongArgs, val)
		}
	}
	if len(latlongArgs) != 6 {
		return config{}, fmt.Errorf("Not enough args.")
	}
	return config{isSouth, isWest, latlongArgs}, nil
}

func main() {
	conf, err := parseArgs(os.Args[1:])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		fmt.Println(USAGE)
		os.Exit(2)

	}
	d_north, m_north, s_north := conf.args[0], conf.args[1], conf.args[2]
	d_east, m_east, s_east := conf.args[3], conf.args[4], conf.args[5]

	ddd_north := toDecimalDegrees(d_north, m_north, s_north)
	ddd_east := toDecimalDegrees(d_east, m_east, s_east)
	if conf.isSouth {
		ddd_north *= -1
	}
	if conf.isWest {
		ddd_east *= -1
	}
	fmt.Printf("%f,%f\n", ddd_north, ddd_east)
}
