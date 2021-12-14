package util

import "fmt"

func Test() {
	fmt.Println("Hello!")
}

func SetOfString(ss []string) map[string]bool {
	set := make(map[string]bool)
	for _, s := range ss {
		set[s] = true
	}
	return set
}

func SetOfInt(ss []int) map[int]bool {
	set := make(map[int]bool)
	for _, s := range ss {
		set[s] = true
	}
	return set
}

type Point2D struct {
	X, Y uint
}

func (p Point2D) String() string {
	return fmt.Sprintf("Point2D[%v, %v]", p.X, p.Y)
}

func Neighbours(xy Point2D, xlim, ylim uint, use_diagonals bool) []Point2D {
	neighbours := make([]Point2D, 0)
	for _, dx := range []int{-1, 0, 1} {
		for _, dy := range []int{-1, 0, 1} {
			if dx == 0 && dy == 0 {
				continue
			}
			if dx != 0 && dy != 0 && !use_diagonals {
				continue
			}
			if (xy.X == 0 && dx < 0) || (xy.X == xlim && dx > 0) {
				continue
			}
			if (xy.Y == 0 && dy < 0) || (xy.Y == xlim && dy > 0) {
				continue
			}
			neighbours = append(neighbours, Point2D{uint(int(xy.X) + dx), uint(int(xy.Y) + dy)})
		}
	}
	return neighbours
}

func CountStrings(ss []string) map[string]uint {
	counts := make(map[string]uint)
	for _, s := range ss {
		counts[s] += 1
	}
	return counts
}

func DedupStrings(ss []string) []string {
	seen := make(map[string]bool)
	dedup := make([]string, 0)
	for _, s := range ss {
		_, ok := seen[s]
		if !ok {
			dedup = append(dedup, s)
		}
		seen[s] = true
	}
	return dedup
}
