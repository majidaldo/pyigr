# etuples usefule here?

class RandomID(str):
    @classmethod
    def mk(cls):
        from uuid import uuid4
        _ =uuid4()
        _ = _.hex
        return cls(_)

    def __repr__(self): return self[:4] # probably good enough


class id:
    def __repr__(self): return self.__class__.__name__
    def __call__(self, i): return i
id = id()


#intermdiate is fmap that 
#create returns that assumes dict output to multiple params

from typing import Callable
from ..connecting import FMap, Connecting
def compose(
        l: Callable, r: Callable,) -> Connecting:
    c = Connecting()
    m = RandomID.mk()
    c.add_func(l, {'return': m })
    # can't 'look inside' to map args
    c.add_func(r, {})  # elegant!
    return c
