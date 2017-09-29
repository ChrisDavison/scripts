package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const BIN_PREFIX = "0b"
const HEX_PREFIX = "0x"

func main() {
	val := os.Args[1]
	// Assume converting from decimal by default
	prefix := ""
	base := 10
	if strings.HasPrefix(val, HEX_PREFIX) {
		prefix = HEX_PREFIX
		base = 16
	} else if strings.HasPrefix(val, BIN_PREFIX) {
		prefix = BIN_PREFIX
		base = 2
	}
	printHexBinDec(parse(val, prefix, base))
}

func parse(val, prefix string, base int) int64 {
	valNoPrefix := strings.TrimPrefix(val, prefix)
	dec, err := strconv.ParseInt(valNoPrefix, base, 64)
	if err != nil {
		log.Fatal(err)
	}
	return dec
}

func printHexBinDec(dec int64) {
	fmt.Printf("%d %s%x %s%b\n", dec, HEX_PREFIX, dec, BIN_PREFIX, dec)
}
