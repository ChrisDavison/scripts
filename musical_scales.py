#!/usr/bin/env python3

def scales(formula):
    import itertools
    import numpy as np
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"] * 2
    steps = np.array([sum(formula[:i]) for i in range(len(formula))])
    for start in notes[:12]:
        idx = notes.index(start)
        these_notes = [notes[n] for n in (steps + idx)]
        print(' '.join(map(lambda x: f"{x:>3}" , these_notes)))


formulas={
    "major": [2, 2, 1, 2, 2, 2, 1],
    "minor": [2, 1, 2, 2, 2, 1, 2]
}
which = "major"
print(which, "scales\n")
scales(formula=formulas[which])
