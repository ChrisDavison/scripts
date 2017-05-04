from prelude.indexable_generator import Indexable

def test_indexable():
    """Asking for an index on a generator should return the appropriate value."""
    i = Indexable(range(1, 10))
    assert i[0] == 1

def test_indexable_after_consuming():
    """An IndexableGenerator can be indexed even after 'consuming'."""
    i = Indexable(range(1, 10))
    values = list(i)
    assert i[0] == 1
