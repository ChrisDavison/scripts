#!/usr/bin/env python
"""Pretty-print $PATH"""
import os

print(os.getenv("PATH").replace(os.pathsep, "\n"))