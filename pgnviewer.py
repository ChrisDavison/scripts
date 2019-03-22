#!/usr/bin/env python3
"""usage: pgnviewer <PGNfile> [query]"""
import os
import shutil
import sys
import textwrap
from pathlib import Path

from docopt import docopt
from chess import Board
from chess.pgn import read_headers, read_game
from chess.svg import board as display


def display(board, title, moves_played):
    os.system("clear")
    print(title)
    print()
    print(board)
    print()
    for chunk in moves_played[-5:]:
        print(chunk)


def choose_game(pgnpath):
    pgn = open(pgnpath, "r")
    games_in_pgn = []
    while True:
        offset = pgn.tell()
        header = read_headers(pgn)
        if header is None:
            break
        game_desc = f"{header['White']} vs {header['Black']}, {header['Result']}"
        games_in_pgn.append((game_desc, offset))

    chosen = games_in_pgn[0]
    if len(games_in_pgn) > 1:
        for i, (head, peek) in enumerate(games_in_pgn):
            print(f"{i+1:3d}: {head}")
        chosen = games_in_pgn[int(input("Choose: ")) - 1]

    pgn.seek(chosen[1])
    return read_game(pgn), chosen[0]


def main():
    args = docopt(__doc__)
    game, title = choose_game(args["<PGNfile>"])
    b = Board()
    moves, annotations = [], []
    for i, move in enumerate(game.mainline_moves()):
        if i%2 == 0:
            moves.append(f"{int(i/2)+1}. {b.san(move)}")
        else:
            moves[-1] += f" {b.san(move)} "
        b.push(move)
        display(b, title, moves)
        annotate = input("> ")
        if annotate:
            annotations.append((int(i/2)+1, annotate))
    print(annotate)
    print("FINISHED")


if __name__ == "__main__":
    sys.exit(main())
