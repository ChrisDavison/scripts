#!/usr/bin/env python3
from mdlc import *


def test_is_valid_web():
    assert is_valid_web("https://httpstat.us/200")
    assert is_valid_web("https://www.google.com")
    assert is_valid_web("https://www.duckduckgo.com")
    
def test_not_valid_web():
    assert not is_valid_web("https://httpstat.us/404")

def test_is_valid_local():
    assert is_valid_local("mdlc.py") == True

def test_not_valid_local():
    assert not is_valid_local("doesnt_exist.py")

def test_get_links():
    tests = [
        ("[test1](https://www.google.com)", ["https://www.google.com"]),
        ("This is [test](https://www.google.com)", ["https://www.google.com"]),
        ("Local [test](mdlc.py)", ["mdlc.py"]),
        ("Local [test](mdlc.py), [another](./asmr.py)", ["mdlc.py", "./asmr.py"])
    ]
    for i, (input, wanted) in enumerate(tests):
        assert get_links(input) == wanted, "Test input: %s" % input
