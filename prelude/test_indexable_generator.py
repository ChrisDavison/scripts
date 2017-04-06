import unittest

from indexable_generator import Indexable

class TestIndexable(unittest.TestCase):
    def testIndex(self):
        """Asking for an index on a generator should return the appropriate value."""
        i = Indexable(range(1, 10))
        self.assertEqual(i[0], 1)

    def testIndexAfterConsume(self):
        """An IndexableGenerator can be indexed even after 'consuming'."""
        i = Indexable(range(1, 10))
        values = list(i)
        self.assertEqual(i[0], 1)
