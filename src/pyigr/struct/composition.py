try: from icecream import ic
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

    @classmethod
    def pylegal(cls):
        while True:
            _ = cls.mk()
            if not _[0].isalpha():
                continue
            else:
                return cls(_[:4])


class id:
    def __repr__(self): return self.__class__.__name__
    def __call__(self, i): return i
id = id()


from typing import Callable
from ..connecting import FMap, Connecting
def compose(
        l: Callable, r: Callable, ) -> Connecting:
    from inspect import signature as sig
    _ = Connecting()
    if  len(sig(l).parameters) == 0 or\
        len(sig(r).parameters) == 0:  
        # seems like the right behavior. you get nothing.
        return _
    
    louts = {p:RandomID.mk() for p in sig(r).parameters }
    if len(louts) == 1:
        (louts,) = louts.values() # take just a param
        _.add_func(l, {'return': louts })
        (rin,) = sig(r).parameters
        _.add_func(r, {rin: louts })
    else:
        _.add_func(l, {'return': louts })
        _.add_func(r, {p:louts[p] for p in sig(r).parameters} )
    return _


# might not have to do this if somehow Set autowires
# def compose_fm(l: FMap, r: FMap) -> Connecting:
#     _ = Connecting()
#     # just find common i{o,i}o ?
#     # kind of already happens with conn.add_fm
#     ic(l.o, l.i)
#     common_oi = l.o & r.i
#     if not common_oi: return _
#     else:
#         common_oi = {oi:RandomID.mk for  oi in common_oi}
#         _.add_func(l.)
#     return common_oi

#def parallel
# just make unique io for each operand