#![allow(dead_code, unused_variables)]
use rand::random;

fn main() {
    let (rn_d, d) = gen::disposition();
    let (rn_a, a) = gen::alignment();
    let (rn_c, c) = gen::class_or_profession();
    let (rn_l, l) = gen::from_where();
    let (rn_do, doing) = gen::doing();
    let (rn_k, k) = gen::know();

    println!(
        "Rolls: [{}, {}, {}, {}, {}, {}]\n",
        rn_d, rn_a, rn_c, rn_l, rn_do, rn_k
    );
    println!("They are a _{}_ _{}_ who _{}_.", a, c, d);
    println!("They are from _{}_", l);
    println!("They are _{}_ and know _{}_.", doing, k);
}

fn rand_choice<'a>(choices: &[&'a str]) -> (usize, &'a str) {
    let choice = random::<usize>() % choices.len();
    (choice, choices[choice])
}

mod gen {
    use super::rand_choice;

    pub fn disposition() -> (usize, &'static str) {
        rand_choice(&[
            "opposes you",
            "dislike you, but will help... for a price",
            "likes you, but won't help for free.",
            "supports you",
        ])
    }

    pub fn alignment() -> (usize, &'static str) {
        rand_choice(&[
            "Good",
            "Lawful",
            "Neutral",
            "Chaotic",
            "Evil",
            "«choose alignment»",
        ])
    }

    pub fn class_or_profession() -> (usize, &'static str) {
        rand_choice(&[
            "Bard/entertainer",
            "Cleric/acolyte",
            "Druid/professional",
            "Fighter/soldier",
            "Paladin/guard/guardian",
            "Ranger/hunter",
            "Thief/criminal",
            "Wizard/scholar",
        ])
    }

    pub fn from_where() -> (usize, String) {
        let choices = &[
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
        ];
        let (mut rn, mut choice) = rand_choice(choices);
        if rn == (choices.len() - 1) {
            (rn, choice) = rand_choice(choices);
            (
                rn,
                format!("{} that no longer exists", &choice[..choices.len() - 1]),
            )
        } else {
            (rn, choice.to_string())
        }
    }

    pub fn doing() -> (usize, &'static str) {
        rand_choice(&[
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
        ])
    }

    pub fn know() -> (usize, &'static str) {
        rand_choice(&[
            "someone who knows something. Roll again to find out what.",
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
        ])
    }
}
