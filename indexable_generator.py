import itertools

class Indexable(object):
    """Class to allow for indexable generators."""
    def __init__(self, it):
        self.it = it

    def __iter__(self):
        self.it, cpy = itertools.tee(self.it)
        return cpy

    def __getitem__(self, index):
        self.it, cpy = itertools.tee(self.it)
        if type(index) is slice:
            return list(itertools.islice(cpy, index.start, index.stop, index.step))
        else:
            return next(itertools.islice(cpy, index, index+1))
