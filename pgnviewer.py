#!/usr/bin/env python
"""usage: pgnviewer <PGNfile> [query]"""
import os
import sys
import textwrap
from pathlib import Path

from docopt import docopt
from chess import Board
from chess.pgn import read_headers, read_game
from chess.svg import board as display


def main():
    args = docopt(__doc__)
    pgn = open(args['<PGNfile>'], 'r')
    games_in_pgn = []
    while True:
        offset = pgn.tell()
        header = read_headers(pgn)
        if header is None:
            break
        game_desc = f"{header['White']} vs {header['Black']}, {header['Result']}"
        games_in_pgn.append((game_desc, offset))

    for i, (head, peek) in enumerate(games_in_pgn):
        print(f"{i+1:3d}: {head}")
    chosen = games_in_pgn[int(input("Choose: "))-1]
    print(chosen[0])

    pgn.seek(chosen[1])
    game = read_game(pgn)
    b = Board()
    os.system('clear')
    moves = []
    idx = 1
    moveiter = game.mainline_moves().__iter__()
    while True:
        try:
            whitemove = next(moveiter)
            blackmove = next(moveiter)
            os.system('clear')
            movestr = f"{idx}. {b.san(whitemove):3s} "
            b.push(whitemove)
            movestr += f"{b.san(blackmove):3s}"
            moves.append(movestr)
            b.push(blackmove)
            print(b)
            print(f"\n{movestr}")
            idx += 1
            input()
        except StopIteration:
            break
    print("FINISHED")


if __name__ == "__main__":
    sys.exit(main())
