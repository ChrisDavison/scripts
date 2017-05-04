#! /usr/bin/env python
import pytest
from conv import *

def test_lb_to_kg_negative():
    assert lb_to_kg(-1) == None

def test_lb_to_kg_0():
    assert lb_to_kg(0) == None

def test_lb_to_kg_positive():
    assert lb_to_kg(1) == 0.454

def test_lb_to_kg_notnumber():
    assert lb_to_kg("test") == None

def test_stonelb_to_kg_negative():
    assert stonelb_to_kg(-1) == None

@pytest.mark.skip(reason="Not implemented")
def test_stonelb_to_kg_0():
    assert False == True

@pytest.mark.skip(reason="Not implemented")
def test_stonelb_to_kg_positive():
    assert False

@pytest.mark.skip(reason="Not implemented")
def test_stonelb_to_kg_notnumber():
    assert False

@pytest.mark.skip(reason="Not implemented")
def test_stonelb_to_kg_notnumber():
    assert False

@pytest.mark.skip(reason="Need full test suite for stone_to_kg")
def test_stone_to_kg():
    assert False

@pytest.mark.skip(reason="Need full test suite for from_kg")
def test_from_kg():
    assert False
