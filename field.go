package main

import (
	"bufio"
	"os"
	"strconv"
	"strings"

	"github.com/pkg/errors"
)

type cell struct {
	now  bool
	next bool
}

// Field represents a game of life playing field
type Field struct {
	row, col int
	field    [][]cell
}

// NewGameOfLife takes a pattern file and propagates the initial field.
func NewGameOfLife(name string) (Field, error) {
	file, err := os.Open(name)
	if err != nil {
		return Field{}, errors.Wrap(err, "Couldn't open file.")
	}
	defer file.Close()
	buf := bufio.NewReader(file)
	f := Field{}
	f.row, f.col, err = readPatternHeader(buf)
	if err != nil {
		return Field{}, errors.Wrap(err, "Parsing header")
	}
	f.field = make([][]cell, f.row)
	for i := range f.field {
		f.field[i] = make([]cell, f.col)
	}
	err = f.create(buf)
	if err != nil {
		return Field{}, errors.Wrap(err, "Creating field")
	}
	return f, nil
}

func readPatternHeader(buf *bufio.Reader) (int, int, error) {
	data, _ := buf.ReadString('\n')
	tokens := strings.Fields(data)
	rows, err := strconv.ParseInt(tokens[0], 10, 64)
	if err != nil {
		return 0, 0, errors.Wrap(err, "Parsing int for numCols")
	}
	cols, err := strconv.ParseInt(tokens[0], 10, 64)

	if err != nil {
		return 0, 0, errors.Wrap(err, "Parsing int for numCols")
	}
	return int(rows), int(cols), nil
}

func (f *Field) create(buf *bufio.Reader) error {
	for i := 0; i < f.row; i++ {
		line, err := buf.ReadString('\n')
		if err != nil {
			return err
		}
		tokens := strings.Fields(line)
		for j := 0; j < f.col; j++ {
			value, _ := strconv.Atoi(tokens[j])
			if value != 0 {
				f.field[i][j].now = true
			}
		}
	}
	return nil
}

func (f *Field) neighbours(curX, curY int) int {
	neigh := 0

	hor := []int{curX - 1, curX, curX + 1}
	ver := []int{curY - 1, curY, curY + 1}

	if hor[1] == 0 {
		hor[0] = f.row - 1
	}
	if ver[1] == 0 {
		ver[0] = f.col - 1
	}

	if hor[2] == f.row {
		hor[2] = 0
	}
	if ver[2] == f.col {
		ver[2] = 0
	}

	for _, h := range hor {
		for _, v := range ver {
			if f.field[h][v].now == true {
				neigh++
			}
		}
	}
	if f.field[curX][curY].now == true {
		neigh--
	}

	return neigh
}

// Tick performs a single iteration of the game of life
func (f *Field) Tick() {
	for i := 0; i < f.row; i++ {
		for j := 0; j < f.col; j++ {
			cur := f.field[i][j].now
			neighbours := f.neighbours(i, j)
			f.field[i][j].next = false
			if (cur == true && neighbours == 2) || neighbours == 3 {
				f.field[i][j].next = true
			}
		}
	}
	for i := 0; i < f.row; i++ {
		for j := 0; j < f.col; j++ {
			f.field[i][j].now = f.field[i][j].next
		}
	}
}

// String satisfies the string interface, for formatted printing.
func (f Field) String() string {
	out := ""
	for i := 0; i < f.row; i++ {
		out += " "
		for j := 0; j < f.col; j++ {
			if f.field[i][j].now == true {
				out += "#"
			} else {
				out += "-"
			}
		}
		out += "\n"
	}
	return out
}
