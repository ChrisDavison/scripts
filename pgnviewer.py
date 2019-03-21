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
    joined_moves = [f"{i+1:2d}.{w}_{b}" for i, (w, b) in enumerate(moves_played)]
    os.system('clear')
    print(title)
    print()
    print(board)
    print()
    s = shutil.get_terminal_size((80, 20))
    ss = min([80, s.columns-2])
    filled = textwrap.fill('-'.join(joined_moves), ss)
    print(filled.replace('-', ' ').replace('_', ' ').strip())


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

    chosen = games_in_pgn[0]
    if len(games_in_pgn) > 1:
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
    isBlack = False
    this_move = []
    for move in game.mainline_moves():
        this_move.append(b.san(move))
        b.push(move)
        if isBlack:
            moves.append(this_move)
            this_move = []
            display(b, chosen[0], moves)
            input()
        isBlack = not isBlack
    print("FINISHED")


if __name__ == "__main__":
    sys.exit(main())
