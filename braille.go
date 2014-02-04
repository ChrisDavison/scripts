package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const alph = " a c bif e d hjg k m lsp o n rtq              w  u x v   z y    "

func NumToBraille(num int64) string {
	s := strconv.FormatInt(num, 2)
	s = strings.Repeat("0", 6-len(s)) + s

	a, b, c := s[4:], s[2:4], s[:2]

	a = strings.Replace(a, "0", ".", -1)
	a = strings.Replace(a, "1", "O", -1)

	b = strings.Replace(b, "0", ".", -1)
	b = strings.Replace(b, "1", "O", -1)

	c = strings.Replace(c, "0", ".", -1)
	c = strings.Replace(c, "1", "O", -1)

	return fmt.Sprintf("%v%v%v", c, b, a)
}

func BrailleToNum(name string) ([]string, []int64) {
	var m []string
	var n []int64
	j := 0

	file, _ := os.Open(name)
	defer file.Close()

	bfile := bufio.NewScanner(file)

	for bfile.Scan() {
		line := bfile.Text()
		tokens := strings.Split(line, ` `)

		if j == 0 {
			m = make([]string, len(tokens))
			n = make([]int64, len(tokens))
			j += 1
		}
		for i, v := range tokens {
			switch v {
			case "..":
				m[i] = "00" + m[i]
			case "O.":
				m[i] = "01" + m[i]
			case ".O":
				m[i] = "10" + m[i]
			case "OO":
				m[i] = "11" + m[i]
			}
		}
	}
	for i, v := range m {
		n[i], _ = strconv.ParseInt(v, 2, 0)
	}
	return m, n
}

func PrintBraille(b []string) {
	var d, e, f string
	for i, _ := range b {
		d += string(b[i][5]) + string(b[i][4]) + " "
		e += string(b[i][3]) + string(b[i][2]) + " "
		f += string(b[i][1]) + string(b[i][0]) + " "
	}
	fmt.Printf("%v\n%v\n%v\n", d, e, f)
}

func main() {
	var fn = flag.String("f", "", "Braille file to Message")
	var ms = flag.String("m", "", "Message to Braille")
	flag.Parse()

	switch {
	case *fn != "":
		brailleToMessage(*fn)
	case *ms != "":
		messageToBraille(*ms)
	default:
		flag.Usage()
	}

	return
}

func brailleToMessage(s string) {
	var msg string

	binary, decimal := BrailleToNum(s)

	for i := 0; i < len(binary); i++ {
		msg += string(alph[decimal[i]])
	}
	fmt.Printf("%v\n", msg)
}

func messageToBraille(s string) {
	braille := make([]string, len(s))
	for i, _ := range braille {
		curLet := strings.Index(alph, string((s)[i]))
		braille[i] = NumToBraille(int64(curLet))
	}
	PrintBraille(braille)
}
