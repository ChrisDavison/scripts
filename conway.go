package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"strconv"
	"time"
)

func main() {
	if len(os.Args) < 4 {
		fmt.Printf("Usage: %v <file> <iterations> <delay>\n", os.Args[0])
		return
	}

	game, err := NewGameOfLife(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	iters, err := strconv.Atoi(os.Args[2])
	if err != nil {
		log.Fatal(err)
	}
	delay, err := strconv.Atoi(os.Args[3])
	if err != nil {
		log.Fatal(err)
	}
	for i := 0; i < iters; i++ {
		clearScreen()
		fmt.Println(game)
		game.Tick()
		time.Sleep(time.Duration(delay) * time.Millisecond)
	}
}

func clearScreen() {
	c := exec.Command("clear")
	c.Stdout = os.Stdout
	c.Run()
}
