import unittest
from listop import *

class TestListop(unittest.TestCase):
    def testCanFlattenListOfLists(self):
        self.assertEqual([1, 2, 3, 4], flatten([[1, 2], [3, 4]]))

    def testCanListAMap(self):
        ls = [1, 2, 3, 4, 5]
        func = lambda x: x*x
        expected = [1, 4, 9, 16, 25]
        self.assertEqual(expected, lmap(func, ls))

    def testChunksWithExactStride(self):
        """Should be able to stride comfortably."""
        inp = [1, 2, 3, 4, 5, 6]
        stride = 3
        expected = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(expected, chunks(inp, stride))

    def testChunksWithRemainder(self):
        """If your stride is too large, just give what's left."""
        inp = [1, 2, 3, 4, 5, 6]
        stride = 4
        expected = [[1, 2, 3, 4], [5, 6]]
        self.assertEqual(expected, chunks(inp, stride))

    def testChunksWithNoStrideIsAnError(self):
        """No stride over something is a failure."""
        inp = [1, 2, 3, 4, 5, 6]
        stride = 0
        self.assertRaises(ValueError, chunks, inp, stride)

    def testChunksWithNoListIsEmpty(self):
        """A stride over nothing is still nothing."""
        inp = []
        stride = 1
        self.assertEqual([], chunks(inp, stride))
