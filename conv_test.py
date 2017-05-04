#! /usr/bin/env python
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
