package main

import (
	"fmt"
	"math/rand"
	"os"
	"time"
)

func main() {
	for _, a := range os.Args {
		if a == "-h" || a == "--help" || a == "help" {
			showHelp()
			os.Exit(0)
		}
	}
	rand.Seed(time.Now().UnixMicro())
	rn_d, d := what_is_their_disposition()
	rn_a, a := what_is_their_alignment()
	rn_c, c := what_class_or_profession_are_they()
	rn_l, l := where_are_they_from()
	rn_do, do := what_they_are_doing()
	rn_k, k := what_they_know()

	fmt.Printf("Rolls: [%d, %d, %d, %d, %d, %d]\n\n", rn_d, rn_a, rn_c, rn_l, rn_do, rn_k)

	fmt.Printf("They are a %s «%s» who %s.\n", a, c, d)
	fmt.Printf("They are from %s\n", l)
	fmt.Printf("They are %s and know %s.\n", do, k)
}

func showHelp() {
	fmt.Println("Generate NPC using d4, d6, d8, d12, and d20")
	fmt.Println("usage: npcgen")
}

func what_is_their_disposition() (int, string) {
	return randChoice([]string{
		"opposes you",
		"dislike you, but will help... for a price",
		"likes you, but won't help for free.",
		"supports you",
	})
}

func what_is_their_alignment() (int, string) {
	return randChoice([]string{
		"Good",
		"Lawful",
		"Neutral",
		"Chaotic",
		"Evil",
		"«choose alignment»",
	})
}

func what_class_or_profession_are_they() (int, string) {
	return randChoice([]string{
		"Bard (entertainer)",
		"Cleric (acolyte)",
		"Druid (professional...baker, blacksmith, farmer etc.))",
		"Fighter (soldier)",
		"Paladin (guard, guardian)",
		"Ranger (hunter)",
		"Thief (criminal)",
		"Wizard (scholar)",
	})
}

func where_are_they_from() (int, string) {
	choices := []string{
		"wherever you're at right now.",
		"a neighboring region.",
		"the same place a PC is from.",
		"a far away place.",
		"a local guild.",
		"an exotic location.",
		"a large island.",
		"an underground or underwater city.",
		"the shadows....",
		"roll again, and that place no longer exists!",
	}
	rn, choice := randChoice(choices)
	if rn == (len(choices) - 1) {
		rn, choice = randChoice(choices)
		choice = choice[:len(choice)-1] + " that no longer exists."
	}

	return rn, choice
}

func what_they_are_doing() (int, string) {
	return randChoice([]string{

		"Seeking a PC",
		"Searching for something",
		"Passing through to somewhere else",
		"Whatever they're trained to do",
		"Running away / hiding from someone / something",
		"Delivering a message",
		"Training (him/herself or someone else)",
		"Carousing",
		"Killing someone, or attempting to",
		"Stealing something, or attempting to",
		"Purchasing / selling something, or attempting to",
		"Investingating something",
	})
}

func what_they_know() (int, string) {
	return randChoice([]string{

		"someone who knows somthing. Roll again to find out what",
		"where someone was taken",
		"who took someone",
		"who the scapegoat is",
		"why no-one is talking about it",
		"how to make someone disappear",
		"how to get into that place",
		"when it's going to happen",
		"who the real killer / thief was",
		"YOUR secret",
		"more about the monster than he should",
		"how to get what they want from you",
		"where it is hidden",
		"the person's true identity",
		"who has it",
		"who wants it",
		"what you did in that last city",
		"who is keeping track of your actions",
		"who those people that just came into town are",
		"Many secrets! Roll 1d4+1 secrets, ignoring rolls of 20",
	})
}

func randChoice(choices []string) (int, string) {
	rn := rand.Intn(len(choices))
	return rn, choices[rn]

}
