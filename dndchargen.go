package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	tables := [][][]int8{
		{
			{15, 15, 15, 8, 8, 8},
			{15, 15, 15, 9, 9, 6},
			{15, 15, 15, 10, 7, 7},
			{15, 15, 15, 11, 6, 6},
		},
		{
			{15, 14, 13, 12, 11, 11},
			{15, 14, 14, 13, 10, 7},
			{15, 14, 14, 14, 7, 7},
			{15, 15, 12, 12, 11, 9},
			{15, 15, 13, 12, 10, 8},
			{15, 15, 13, 13, 9, 8},
		}, {
			{15, 15, 13, 13, 10, 6},
			{15, 15, 14, 10, 9, 9},
			{15, 15, 14, 11, 9, 8},
			{15, 15, 14, 11, 10, 6},
			{15, 15, 14, 12, 8, 7},
			{15, 15, 14, 13, 7, 6},
		}, {
			{14, 14, 14, 13, 12, 8},
			{14, 14, 14, 13, 13, 6},
			{14, 14, 14, 14, 9, 9},
			{14, 14, 14, 14, 11, 6},
			{15, 13, 13, 13, 12, 11},
			{15, 14, 13, 13, 10, 10},
			{15, 14, 14, 11, 10, 10},
			{15, 15, 12, 12, 12, 7},
		}, {
			{16, 13, 12, 12, 11, 10},
			{16, 13, 13, 12, 11, 9},
			{16, 13, 13, 13, 10, 8},
			{16, 14, 12, 10, 10, 10},
			{16, 14, 12, 11, 11, 9},
			{16, 14, 13, 10, 10, 9},
			{16, 14, 13, 11, 10, 8},
			{16, 14, 13, 13, 8, 7},
		}, {
			{16, 14, 14, 10, 9, 7},
			{16, 14, 14, 11, 8, 7},
			{16, 15, 11, 11, 11, 7},
			{16, 15, 12, 10, 10, 6},
			{16, 15, 12, 11, 8, 8},
			{16, 15, 13, 10, 9, 6},
			{16, 15, 13, 11, 8, 6},
			{16, 15, 14, 9, 7, 6},
		}}

	rand.Seed(time.Now().Unix())
	whichTable := rand.Intn(len(tables))
	whichRow := rand.Intn(len(tables[whichTable]))
	fmt.Printf("Rolled: %v, %v\n\n", whichTable, whichRow)
	fmt.Println(tables[whichTable][whichRow])
}
