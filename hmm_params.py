import csv
import ast
import numpy as np


def read(filename):
    hmm_params = []

    with open(filename, 'rt') as f:
        for row in csv.reader(f, delimiter=';'):
            hmm_params.append(np.array(ast.literal_eval(row[0])))

    return hmm_params
