from prelude.listop import *
import pytest

def testCanFlattenListOfLists():
    assert [1, 2, 3, 4] == flatten([[1, 2], [3, 4]])

def testCanListAMap():
    ls = [1, 2, 3, 4, 5]
    func = lambda x: x*x
    expected = [1, 4, 9, 16, 25]
    assert expected == lmap(func, ls)

def testChunksWithExactStride():
    """Should be able to stride comfortably."""
    inp = [1, 2, 3, 4, 5, 6]
    stride = 3
    expected = [[1, 2, 3], [4, 5, 6]]
    assert expected == chunks(inp, stride)

def testChunksWithRemainder():
    """If your stride is too large, just give what's left."""
    inp = [1, 2, 3, 4, 5, 6]
    stride = 4
    expected = [[1, 2, 3, 4], [5, 6]]
    assert expected == chunks(inp, stride)

def testChunksWithNoStrideIsAnError():
    """No stride over something is a failure."""
    inp = [1, 2, 3, 4, 5, 6]
    stride = 0
    with pytest.raises(ValueError):
        chunks(inp, stride)

def testChunksWithNoListIsEmpty():
    """A stride over nothing is still nothing."""
    inp = []
    stride = 1
    assert [] == chunks(inp, stride)
