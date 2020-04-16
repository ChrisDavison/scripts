package main

import (
	"fmt"
	"os"
	"path"
	"strconv"
)

const (
	errBadUsage int = iota + 1
	errUnknownUnit
	errParseValue
)

// Mass represents a weight in kilos
type Mass float64

func (m Mass) String() string {
	valueKg := m
	valueLb := valueKg * 2.2
	valueSt := valueKg * 2.2 / 14
	return fmt.Sprintf("%.2fkg %.2fst %.2flb", valueKg, valueSt, valueLb)
}

// NewMass creates a mass
func NewMass(value float64, unit string) (*Mass, error) {
	var m Mass
	if unit == "kg" {
		m = Mass(value)
	} else if unit == "lb" {
		m = Mass(value / 2.2)
	} else if unit == "st" {
		m = Mass(value * 14 / 2.2)
	} else {
		return nil, fmt.Errorf("Unknown unit %v", unit)
	}
	return &m, nil
}

func usage() {
	appname := path.Base(os.Args[0])
	fmt.Fprintf(os.Stderr, "usage: %s <value> <kg|lb|st>\n", appname)
}

func main() {
	args := os.Args[1:]
	if len(args) < 2 {
		usage()
		os.Exit(errBadUsage)
	}
	start := 118.0
	unit := args[1]
	value, err := strconv.ParseFloat(args[0], 16)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error parsing value ", value)
		os.Exit(errParseValue)
	}
	m, err := NewMass(value, unit)
	if err != nil {
		usage()
		os.Exit(errUnknownUnit)
	}
	diff := start - float64(*m)
	fmt.Printf("%s (lost %.2fkg)\n", m, diff)
}
