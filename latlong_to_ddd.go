package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	args := os.Args[1:]
	if len(args) != 6 {
		fmt.Fprintln(os.Stderr, "usage: latlong_to_ddd D_north M_north S_north D_east M_east S_east")
		os.Exit(1)
	}
	d_north, _ := strconv.ParseFloat(args[0], 10)
	m_north, _ := strconv.ParseFloat(args[1], 10)
	if m_north < 0 {
		m_north *= -1
	}

	s_north, _ := strconv.ParseFloat(args[2], 10)
	if s_north < 0 {
		s_north *= -1
	}

	d_east, _ := strconv.ParseFloat(args[3], 10)
	m_east, _ := strconv.ParseFloat(args[4], 10)
	if m_east < 0 {
		m_east *= -1
	}
	s_east, _ := strconv.ParseFloat(args[5], 10)
	if s_east < 0 {
		s_east *= -1
	}

	ddd_north := d_north + ((m_north + (s_north / 60)) / 60)
	ddd_east := d_east + ((m_east + (s_east / 60)) / 60)
	fmt.Printf("%f,%f\n", ddd_north, ddd_east)
}
