try: import icecream as ic
except ImportError: pass

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


from typing import Callable
from ..connecting import FMap, Connecting
def compose(
        l: Callable, r: Callable, ) -> Connecting:
    _ = Connecting()
    from inspect import signature as sig
    louts = {p:RandomID.mk() for p in sig(r).parameters  }
    if len(louts) == 1:
        (louts,) = louts.values() # take just a param
        _.add_func(l, {'return': louts })
        (rin,) = sig(r).parameters
        _.add_func(r, {rin: louts })
    else:
        _.add_func(l, {'return': louts })
        _.add_func(r, {p:louts[p] for p in sig(r).parameters} )
    return _
