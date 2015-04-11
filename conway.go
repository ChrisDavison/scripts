package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
    "os/exec"
    "strconv"
    "strings"
    "time"
)

type Cell struct {
    now  bool
    next bool
}

type Field struct {
    row, col int
    field    [][]Cell
}

func (f *Field) Init(name string) {
    file, err := os.Open(name)
    if err != nil {
        log.Fatalf("Error opening: %v\n", name)
    }
    defer file.Close()

    bFile := bufio.NewReader(file)
    data, _ := bFile.ReadString('\n')
    tokens := strings.Fields(data)
    intTokens := make([]int, len(tokens))

    for i := range tokens {
        intTokens[i], _ = strconv.Atoi(tokens[i])
    }

    f.row, f.col = intTokens[0], intTokens[1]
    f.field = make([][]Cell, f.row)

    for i := range f.field {
        f.field[i] = make([]Cell, f.col)
    }

    f.create(bFile)
}

func (f *Field) create(bFile *bufio.Reader) {
    for i := 0; i < f.row; i++ {
        line, _ := bFile.ReadString('\n')
        tokens := strings.Fields(line)

        for j := 0; j < f.col; j++ {
            value, _ := strconv.Atoi(tokens[j])

            if value == 0 {
                f.field[i][j].now = false
            } else {
                f.field[i][j].now = true
            }
        }
    }
}

func (f *Field) Neighbours(curX, curY int) int {
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
                neigh += 1
            }
        }
    }
    if f.field[curX][curY].now == true {
        neigh -= 1
    }

    return neigh
}

func (f *Field) Tick() {
    for i := 0; i < f.row; i++ {
        for j := 0; j < f.col; j++ {
            cur := f.field[i][j].now
						neighbours := f.Neighbours(i, j)
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

func (f *Field) Show() {
    for i := 0; i < f.row; i++ {
        fmt.Printf(" ")
        for j := 0; j < f.col; j++ {
            if f.field[i][j].now == true {
                fmt.Printf("#")
            } else {
                fmt.Printf("-")
            }
        }
        fmt.Printf("\n")
    }
}

func main() {
    var game Field

    if len(os.Args) < 4 {
        fmt.Printf("Usage: %v <file> <iterations> <delay>\n", os.Args[0])
        return
    }

    game.Init(os.Args[1])
    iters, _ := strconv.Atoi(os.Args[2])
    delay, _ := strconv.Atoi(os.Args[3])
    for i := 0; i < iters; i++ {
        c := exec.Command("clear")
        c.Stdout = os.Stdout
        c.Run()
        game.Show()
        game.Tick()
        time.Sleep(time.Duration(delay) * time.Millisecond)
    }
}
