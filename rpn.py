#!/usr/bin/env python
"""
usage: rpn.py [-v] CALCULATION...

Supports operations:
+ 
- 
\\ (divide) 
* (multiply)
** (power)
sin, tan, cos
R (to radians)
D (to degrees)

options:
    -v     Print each stage of the stack
    -h     Show this message
"""
import math as m
import os
import sys
from pathlib import Path


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
        except:
            return False

    def __iter__(self):
        functions = {
            '+': (False, lambda x, y: x + y),
            '-': (False, lambda x, y: x - y),
            '*': (False, lambda x, y: x * y),
            '**': (False, lambda x, y: x ** y),
            '\\': (False, lambda x, y: x / y),
            'R': (True, lambda x: x * m.pi / 180),
            'D': (True, lambda x: x * 180 / m.pi),
            'cos': (True, m.cos),
            'sin': (True, m.sin),
            'tan': (True, m.tan),
            'pow': (True, m.pow)
        }
        for element in self.calculation:
            if self.is_numeric(element):
                self.stack.append(float(element))
                yield ' '.join(map(str, self.stack)), '<'
            else:
                yield ' '.join(map(str, self.stack)), element
                unary, operation = functions[element]
                if unary:
                    self._unary(operation)
                else:
                    self._binary(operation)
        if len(self.stack) > 1:
            raise Exception("Not enough operations.  Stack still has multiple values")
        self.result = self.stack[0]

    def _unary(self, operation):
        x = self.stack.pop()
        self.stack.append(operation(x))

    def _binary(self, operation):
        y, x = self.stack.pop(), self.stack.pop()
        self.stack.append(operation(x, y))
        

def main():
    args = sys.argv[1:]
    verbose = False
    if '-v' in args:
        verbose = True
        args.remove('-v')
    rpn = RPN("5 6 3 * 5 + +")
    if args:
        rpn = RPN(' '.join(args))
    for stack, operation in rpn:
        if verbose:
            print(stack, operation)
    print(f"RESULT: {rpn.result}")


if __name__ == "__main__":
    sys.exit(main())
