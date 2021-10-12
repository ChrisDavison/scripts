#!/usr/bin/env python3
from pathlib import Path
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from toolz import groupby


def similarities_for_folder_contents(folder):
    """BLAH"""
    files = [
        f.stem
        for f in folder.rglob("*")
        if not f.is_dir() and re.match(r".*\(\d+", str(f))
    ]
    if not files:
        return []
    vec = TfidfVectorizer()
    mat = vec.fit_transform(files)
    sim = set()
    for i, name in enumerate(files):
        simil = cosine_similarity(mat[i], mat)[0]
        for name2 in files:
            if name == name2:
                continue
            name1, name2 = sorted([name, name2])
            # print(name1, name2, simil[j])
            # return []
            sim.add((name1, name2, simil[i]))
    return sorted(list(sim), key=lambda x: x[2], reverse=True)


def calc_similarities():
    """BLAH"""
    simils = dict()
    dirs_mean_simil = []
    for subdir in Path("E:/Dropbox/guitar/tabs").rglob("*"):
        if not subdir.is_dir() or len(subdir.stem) == 1:
            continue
        sim = similarities_for_folder_contents(subdir)
        simils[subdir] = sim
        dirs_mean_simil.append((subdir.stem, np.mean([x[2] for x in sim] + [0])))
    return sorted(
        [a for a in dirs_mean_simil if a[1] > 0.1], key=lambda x: x[1], reverse=True
    )


artists_similarity = calc_similarities()
