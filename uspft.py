#!/usr/bin/env python

scores = {
    "pullups": [(4,20), (5,23), (5,23), (5,23), (5,21), (5,20), (5,19), (4,19)],
    "crunches": [
        (70,105),
        (70,110),
        (70,115),
        (70,115),
        (70,110),
        (65,105),
        (50,100),
        (40,100),
    ],
    "run": [
        (18 * 60,27 * 60 + 40),
        (18 * 60,27 * 60 + 40),
        (18 * 60,28 * 60 + 00),
        (18 * 60,28 * 60 + 40),
        (18 * 60,28 * 60 + 40),
        (18 * 60 + 30,29 * 60 + 40),
        (19 * 60,30 * 60 + 40),
        (19 * 60 + 30,33 * 60 + 40),
    ],
}

def pullup_score(lower, upper):
    pullups = int(input("Pullups: "))
    if pullups > upper:
        return 100
    elif pullups < lower:
        return 0
    else:
        range = upper - lower
        pct_through = (pullups - lower) / range * 100
        return int(pct_through)


def run_score(lower, upper):
    runtime = input("Runtime: ")
    hh, mm = [int(v) for v in runtime.split(":")]
    runtime = hh*60 + mm
    if runtime > upper:
        return 100
    elif runtime < lower:
        return 0
    else:
        range = upper - lower
        pct_through = (runtime - lower) / range * 100
        return int(100-pct_through)



def crunch_score(lower, upper):
    crunches = int(input("Crunches: "))
    if crunches > upper:
        return 100
    elif crunches < lower:
        return 0
    else:
        range = upper - lower
        pct_through = (crunches - lower) / range * 100
        return int(pct_through)


def score_bracket(age):
    if age >= 17 and age <= 20:
        return 0
    elif age >= 21 and age <= 25:
        return 1
    elif age >= 26 and age <= 30:
        return 2
    elif age >= 31 and age <= 35:
        return 3
    elif age >= 36 and age <= 40:
        return 4
    elif age >= 41 and age <= 45:
        return 5
    elif age >= 46 and age <= 50:
        return 6
    elif age >= 51:
        return 7
    else:
        print("Age must be >= 17")
        age = input("Age: ")
        return score_bracket(age)


def main():
    age = 30
    bracket = score_bracket(age)
    pullup = pullup_score(*scores['pullups'][bracket])
    print(pullup)
    crunch = crunch_score(*scores['crunches'][bracket])
    print(crunch)
    run = run_score(*scores['run'][bracket])
    print(run)
    print("Total:", pullup + crunch + run, "out of 300")


if __name__ == "__main__":
    main()
