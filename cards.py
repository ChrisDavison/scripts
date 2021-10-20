#!/usr/bin/env python3
import numpy as np
import random
from collections import Counter
from itertools import islice
import sys

from dataclasses import dataclass
from typing import List, Dict


random.seed(None)
ALL_CARDS = [(suit, number) for number in range(1, 14) for suit in "CHSD"]


@dataclass
class Hand:
    def __init__(self, cards):
        self.hand = cards
        self.suits = Counter(s for s, n in cards)
        self.nums = Counter(int(n) for s, n in cards)
        self.number_counts = list(self.nums.values())
        self.n_unique_nums = len(self.nums.keys())

    def add(self, other):
        assert len(self.hand) < 5, "Can't have more than 5 cards"
        if isinstance(other, list):
            assert len(self.hand) + len(other) <= 5, "Can't have more than 5 cards"
            self.hand.extend(other)
        else:
            assert len(self.hand) <= 4, "Can't have more than 5 cards"
            self.hand.extend([other])
        self.suits = Counter(s for s, n in self.hand)
        self.nums = Counter(int(n) for s, n in self.hand)
        self.number_counts = list(self.nums.values())
        self.n_unique_nums = len(self.nums.keys())

    @staticmethod
    def random():
        return Hand(random.choices(ALL_CARDS, k=5))

    def __str__(self):
        return "Hand(" + " ".join(f"{suit}{number}" for suit, number in self.hand) + ")"

    def __repr__(self):
        return self.__str__()


    def is_full_house(self):
        return self.n_unique_nums == 2 and 3 in self.number_counts

    def is_flush(self):
        return len(self.suits.keys()) == 1

    def is_straight_flush(self):
        return self.is_flush() and self.is_straight()

    def is_straight(self):
        nums = sorted(self.nums)
        if len(nums) < 5:
            return False
        return nums[0] == nums[1] - 1 == nums[2] - 2 == nums[3] - 3 == nums[4] - 4

    def is_pair(self):
        return self.n_unique_nums == 4 and 2 in self.number_counts

    def is_twopair(self):
        nums = list(self.number_counts)
        if 2 in nums:
            nums.remove(2)
        return 2 in nums

    def is_three_of_a_kind(self):
        return self.n_unique_nums == 3 and 3 in self.number_counts

    def is_four_of_a_kind(self):
        return self.n_unique_nums == 2 and 4 in self.number_counts


def random_hand_generator(n=None):
    generated = 0
    while True:
        yield Hand.random()
        generated += 1
        if n and generated == n:
            break


def prob_of_future_hands(current):
    remaining = remaining_cards(current)
    print(len(remaining))
    probs = {
        "pair": prob_getting_pair(current),
        "two_pair": prob_getting_two_pair(current),
        "three_of_a_kind": prob_getting_three_of_a_kind(current),
        "four_of_a_kind": prob_getting_four_of_a_kind(current),
        "full_house": prob_getting_full_house(current),
        "flush": prob_getting_flush(current),
        "straight": prob_getting_straight(current),
        "straight_flush": prob_getting_straight_flush(current),
    }


def remaining_cards(current):
    all_cards = ALL_CARDS.copy()
    # print(len(all_cards))
    for card in current.hand:
        all_cards.remove(card)
    return all_cards


def prob_getting_pair(current):
    # if current.is_pair():
    #     return 1
    # else:
    #     if len(current.hand) == 5:
    #         return 0
    #     remaining = remaining_cards(current)
    #     return prob_getting_pair()
    pass


def prob_getting_two_pair(current):
    pass


def prob_getting_three_of_a_kind(current):
    pass


def prob_getting_four_of_a_kind(current):
    pass


def prob_getting_full_house(current):
    pass


def prob_getting_flush(current):
    suits = [s for s, _ in current.hand]
    if not all([s == suits[0] for s in suits]):
        return 0
    if len(suits) == 5:
        return 1
    remaining = remaining_cards(current)
    remaining_suit = [r for r in remaining if r[0] == suits[0]]
    diff = 5 - len(current.hand)
    return (len(remaining_suit) - diff - 1) / len(remaining)


def prob_getting_straight(current):
    pass


def prob_getting_straight_flush(current):
    suits = [s for s, _ in current]
    if not all([s == suits[0] for s in suits]):
        return 0
    pass


# gen = random_hand_generator()
# hand = next(gen)
# hand = Hand([("C", 12), ("H", 12)])
# print(hand)
# print(prob_of_future_hands(hand))

# print(prob_getting_flush(hand))
# print(prob_getting_flush(Hand([("H", 1)])))

how_many_hands = 1_000_000
n_pairs = 0
n_twos = 0
n_threes = 0
n_fours = 0
n_full = 0
n_straight = 0
n_straightflush = 0
n_flush = 0
percents = list(np.linspace(0, how_many_hands, 11))

rng = np.random.default_rng()
choices = rng.choice(ALL_CARDS, (5, 5))
hands = [Hand(choices.tolist()) for choices in rng.choice(ALL_CARDS, (how_many_hands, 5))]

n_pairs = sum(1 for hand in hands if hand.is_pair())
n_twos = sum(1 for hand in hands if hand.is_twopair())
n_threes = sum(1 for hand in hands if hand.is_three_of_a_kind())
n_fours = sum(1 for hand in hands if hand.is_four_of_a_kind())
n_flush = sum(1 for hand in hands if hand.is_flush())
n_straight = sum(1 for hand in hands if hand.is_straight())
n_straightflush = sum(1 for hand in hands if hand.is_straight_flush())
n_full = sum(1 for hand in hands if hand.is_full_house())

for hand in hands:
    if hand.is_pair():
        n_pairs += 1
    if hand.is_twopair():
        n_twos += 1
    if hand.is_three_of_a_kind():
        n_threes += 1
    if hand.is_four_of_a_kind():
        n_fours += 1
    if hand.is_flush():
        n_flush += 1
    if hand.is_straight():
        n_straight += 1
    if hand.is_straight_flush():
        n_straightflush += 1
    if hand.is_full_house():
        n_full += 1

print("\r", end="")
print(f"Pair:           {n_pairs/how_many_hands * 100:.2f}%")
print(f"Two Pair:       {n_twos/how_many_hands * 100:.2f}%")
print(f"Threes:         {n_threes/how_many_hands * 100:.2f}%")
print(f"Full House:     {n_full/how_many_hands * 100:.2f}%")
print(f"Four:           {n_fours/how_many_hands * 100:.2f}%")
print(f"Flush:          {n_flush/how_many_hands * 100:.2f}%")
print(f"Straight:       {n_straight/how_many_hands * 100:.2f}%")

