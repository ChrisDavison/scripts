package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"

	kingpin "gopkg.in/alecthomas/kingpin.v2"
)

const (
	binPrefix = "0b"
	hexPrefix = "0x"
)

func main() {
	val := kingpin.Arg("VALUE", "Decimal, binary, or hex value (with appropriate prefix)").Required().String()
	mode := kingpin.Flag("mode", "Which format to print [all, hex, bin, dec]").
		Short('m').Default("all").String()
	kingpin.Parse()
	prefix := ""
	base := 10
	if strings.HasPrefix(*val, hexPrefix) {
		prefix = hexPrefix
		base = 16
	} else if strings.HasPrefix(*val, binPrefix) {
		prefix = binPrefix
		base = 2
	}
	printHexBinDec(parse(*val, prefix, base), *mode)
}

func parse(val, prefix string, base int) int64 {
	valNoPrefix := strings.TrimPrefix(val, prefix)
	dec, err := strconv.ParseInt(valNoPrefix, base, 64)
	if err != nil {
		log.Fatal(err)
	}
	return dec
}

func printHexBinDec(dec int64, mode string) {
	if mode == "all" {
		fmt.Printf("%d %s%x %s%b\n", dec, hexPrefix, dec, binPrefix, dec)
	} else if mode == "hex" {
		fmt.Printf("%s%x\n", hexPrefix, dec)
	} else if mode == "bin" {
		fmt.Printf("%s%b\n", binPrefix, dec)
	} else {
		fmt.Printf("%d\n", dec)
	}
}
