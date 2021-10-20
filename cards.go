package main

import (
	"fmt"
	"math/rand"
	"sort"
)

func main() {
	var hand Hand
	n_flush := 0
	n_straight := 0
	n_straight_flush := 0
	n_hands := 1_000_000
	n_pair, n_twopair, n_threes, n_fours, n_fullhouse := 0, 0, 0, 0, 0
	for i := 0; i < n_hands; i++ {
		hand = random_hand()
		if hand.IsStraight() {
			n_straight += 1
		}
		if hand.IsFlush() {
			n_flush += 1
		}
		if hand.IsStraightFlush() {
			n_straight_flush += 1
		}
		if hand.IsPair() {
			n_pair += 1
		}
		if hand.IsTwoPair() {
			n_twopair += 1
		}
		if hand.IsThreeOfAKind() {
			n_threes += 1
		}
		if hand.IsFourOfAKind() {
			n_fours += 1
		}
		if hand.IsFullHouse() {
			n_fullhouse += 1
		}
		if false {
			fmt.Println(hand)
		}
	}
	fmt.Printf("%v hands\n", n_hands)
	fmt.Printf("%v pair => %.2f%%\n", n_pair, percent(n_pair, n_hands))
	fmt.Printf("%v two_pair => %.2f%%\n", n_twopair, percent(n_twopair, n_hands))
	fmt.Printf("%v three_of => %.2f%%\n", n_threes, percent(n_threes, n_hands))
	fmt.Printf("%v straight => %.2f%%\n", n_straight, percent(n_straight, n_hands))
	fmt.Printf("%v flush => %.2f%%\n", n_flush, percent(n_flush, n_hands))
	fmt.Printf("%v house => %.2f%%\n", n_fullhouse, percent(n_fullhouse, n_hands))
	fmt.Printf("%v four_of => %.2f%%\n", n_fours, percent(n_fours, n_hands))
	fmt.Printf("%v straight flush => %.2f%%\n", n_straight_flush, percent(n_straight_flush, n_hands))
}

func percent(num, denom int) float64 {
	return float64(num) / float64(denom) * 100
}

type Card struct {
	suit byte
	num  int
}

func (c Card) String() string {
	return fmt.Sprintf("%s%d", string(c.suit), c.num)
}

type Hand struct {
	hand    [5]Card
	cardMap map[int]int
}

func (h Hand) String() string {
	return fmt.Sprintf("<%s %s %s %s %s>",
		h.hand[0],
		h.hand[1],
		h.hand[2],
		h.hand[3],
		h.hand[4],
	)
}

func (h *Hand) MakeCardMap() {
	nums := make(map[int]int)
	for _, card := range h.hand {
		nums[card.num] += 1
	}
	h.cardMap = nums
}

func (h Hand) IsStraight() bool {
	var nums = make([]int, 5)
	for i, card := range h.hand {
		nums[i] = card.num
	}
	sort.Ints(nums)
	prev := nums[0]
	for _, num := range nums[1:] {
		if num != prev+1 {
			return false
		}
		prev = num
	}
	return true
}

func (h Hand) IsFlush() bool {
	first := h.hand[0].suit
	for _, card := range h.hand[1:] {
		if card.suit != first {
			return false
		}
	}
	return true
}

func (h Hand) IsStraightFlush() bool {
	return h.IsStraight() && h.IsFlush()
}

func (h Hand) IsPair() bool {

	found_pair := false
	for _, n_num := range h.cardMap {
		if n_num == 2 && !found_pair {
			found_pair = true
		} else if n_num == 2 {
			return false
		}
	}
	return found_pair
}

func (h Hand) IsTwoPair() bool {
	found_pair := false
	for _, n_num := range h.cardMap {
		if n_num == 2 && !found_pair {
			found_pair = true
		} else if n_num == 2 {
			return true
		}
	}
	return false
}

func (h Hand) IsThreeOfAKind() bool {
	for _, n_num := range h.cardMap {
		if n_num == 3 {
			return true
		}
	}
	return false
}

func (h Hand) IsFourOfAKind() bool {
	for _, n_num := range h.cardMap {
		if n_num == 4 {
			return true
		}
	}
	return false
}

func (h Hand) IsFullHouse() bool {
	return h.IsPair() && h.IsThreeOfAKind()
}

func random_hand() Hand {
	suits := []byte{'C', 'H', 'S', 'D'}

	var cards [5]Card
	// fmt.Println(num)

	n := 0
	for {
		rand_suit := suits[rand.Intn(4)]
		rand_card := rand.Intn(13)
		temp := Card{rand_suit, rand_card}
		for _, card := range cards {
			if card == temp {
				continue
			}
		}
		cards[n] = temp
		n += 1
		if n == 5 {
			break
		}
	}
	h := Hand{cards, make(map[int]int)}
	h.MakeCardMap()
	return h
}
