#!/usr/bin/env python3
"""Reverse Polish Notation calculator

Supports operations:
    +, -, \\, *, **, sin, tan, cos, R (to radians), D (to degrees)

If using divide from command line, must wrap args in '', e.g. ('9 3 \\')

usage: rpn.py [-v] CALCULATION...

options:
    -v     Print each stage of the stack
    -h     Show this message
"""
import math as m
import sys


class RPN:
    def __init__(self, calculation):
        self.calculation = calculation.split()
        self.stack = []
        self.result = None

    def __str__(self):
        return "Not implemented"

    def is_numeric(self, val):
        try:
            float(val)
            return True
        except Exception as E:
            print(E, file=sys.stderr)
            return False

    def __iter__(self):
        functions = {
            "+": (False, lambda x, y: x + y),
            "-": (False, lambda x, y: x - y),
            "*": (False, lambda x, y: x * y),
            "**": (False, lambda x, y: x ** y),
            "\\": (False, lambda x, y: x / y),
            "R": (True, lambda x: x * m.pi / 180),
            "D": (True, lambda x: x * 180 / m.pi),
            "cos": (True, m.cos),
            "sin": (True, m.sin),
            "tan": (True, m.tan),
            "pow": (True, m.pow),
        }
        for element in self.calculation:
            if self.is_numeric(element):
                self.stack.append(float(element))
                yield " ".join(map(str, self.stack)), "<"
            else:
                yield " ".join(map(str, self.stack)), element
                unary, operation = functions[element]
                if unary:
                    self._unary(operation)
                else:
                    self._binary(operation)
        if len(self.stack) > 1:
            raise Exception("Not enough operations.  Stack still has multiple values")
        self.result = self.stack[0]

    def evaluate(self):
        for _ in self:
            continue

    def _unary(self, operation):
        x = self.stack.pop()
        self.stack.append(operation(x))

    def _binary(self, operation):
        y, x = self.stack.pop(), self.stack.pop()
        self.stack.append(operation(x, y))


def __interactive():
    print("Type 'exit' or 'quit' to exit")
    while True:
        i = input("> ")
        if "quit" in i or "exit" in i:
            break
        yield i
    print("EXITING")


def display_equation_steps(rpn):
    for stack, operation in rpn:
        print(stack, operation)
    return rpn


def main():
    args = sys.argv[1:]
    verbose = False
    if "-v" in args:
        verbose = True
        args.remove("-v")
    if "-h" in args:
        print(__doc__)
        sys.exit(0)
    equations = __interactive() if not args else [" ".join(args)]
    for eqn in equations:
        rpn = RPN(eqn)
        if verbose:
            display_equation_steps(rpn)
        else:
            rpn.evaluate()
        print(rpn.result)


if __name__ == "__main__":
    sys.exit(main())
