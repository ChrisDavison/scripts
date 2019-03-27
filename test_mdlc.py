#!/usr/bin/env python3
from mdlc import *


def test_is_valid_web():
    """Test both valid and invalid web URLs."""
    assert is_valid_web("https://httpstat.us/200")
    assert is_valid_web("https://www.google.com")
    assert is_valid_web("https://www.duckduckgo.com")
    assert not is_valid_web("https://httpstat.us/404")
    assert not is_valid_web("README.md")
    assert not is_valid_web("README.md#anchor")


def test_is_valid_local():
    """Test both valid and invalid local URLs."""
    assert is_valid_local("mdlc.py") == True
    assert is_valid_local("README.md") == True
    assert is_valid_local("README.md#scripts") == True
    assert not is_valid_local("doesnt_exist.py")
    assert not is_valid_local("https://www.google.com")
    assert not is_valid_local("https://www.httpstat.us/200")


def test_get_links():
    """Test extract links from a text."""
    assert get_links("") == []
    assert get_links("[test1](https://www.google.com)") == ["https://www.google.com"]
    assert get_links("Local [test](mdlc.py)") == ["mdlc.py"]
    assert get_links("- Local [test](mdlc.py)") == ["mdlc.py"]
    assert get_links("[ref]: https://www.google.com") == ["https://www.google.com"]

    inp, exp = "This is [test](https://www.google.com)", ["https://www.google.com"]
    assert get_links(inp) == exp

    inp, exp = "Local [test](mdlc.py)), [another](./asmr.py)", ["mdlc.py", "./asmr.py"]
    assert get_links(inp) == exp

    inp, exp = "Local with anchor [test](README.md#anchor)", ["README.md#anchor"]
    assert get_links(inp) == exp

    inp = "[test](README.md#anchor) [ref][]\n    [ref]: https://www.google.com"
    exp = ["README.md#anchor", "https://www.google.com"] 
    assert get_links(inp) == exp


def test_handling_anchors():
    """Test removal of markdown anchors from local links"""
    assert trim_md_anchor("file.md#anchor") == "file.md"
    assert trim_md_anchor("file.md#") == "file.md"
    assert trim_md_anchor("file.md#file.md") == "file.md"
    assert trim_md_anchor("file.md") == "file.md"


def test_invalid_links_in_file():
    inp = "README.md"
    exp = [
            "https://www.google.com",
            "https://www.duckduckgo.com",
            "https://www.httpstat.us/404"
    ]
    assert set(get_links_from_file("README.md")) == set(exp)
    assert mdlc("README.md") == ["https://www.httpstat.us/404"]

