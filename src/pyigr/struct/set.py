import profile
try: from icecream import ic
except ImportError: pass

def dataclass(c):
    from dataclasses import dataclass
    return dataclass(frozen=True)(c)

from ..connecting import Connecting, types as ctypes, FMap
from .composition import id


class SetMap: 
    """
    'converts' what was established in Connecting
    to just mappings from sets to sets.
    """
    def __init__(self, fm: FMap):
        self.fm = fm
    def __repr__(self):
        return '*'+repr(self.fm)

    def __call__(self, values: dict):
        return self.fm(values)

    #def funcitions: id, partial set



#  TODO need a function that creates partial sets {x,y}->{x}

class Sets:#(FMap or Connecting) make it look like FMap or Connecting? 
    def __init__(self, con: Connecting):
        self.con = Connecting(name=f'Set({con.name})' if con.name else None)
        S = ctypes.Set  # to emphasize
        for fm in con.fmaps:
            # sets -> sets
            self.con.add_func(SetMap(fm), {'values': (fm.i) , 'return': ((fm.o),) } ) # interesting...
            self.con.add_func(id, {'i': (fm.i), 'return': ((fm.i),) } ) # # interesting nesting
            self.con.add_func(id, {'i': (fm.o), 'return': ((fm.o),) } ) # 
            for i in fm.i: self.con.add_func(id)
            for o in fm.o: self.con.add_func(id)
    
    def __repr__(self):     return repr(self.con)
    def _display_(self):    return self.con._display_()

    from functools import cached_property
    @cached_property
    def hom(self):# -> Connecting:
        def _():
            for fm in self.con.fmaps:
                yield fm.i, fm.o
        
        #from networkx import all_simple_edge_paths  # to more directly represent composition? it would look just like hom
        #from networkx import all_simple_paths
        #_ = all_simple_paths(self.con.graph, self.con.fmaps[0], self.con.fmaps[2],)
        _ = list(_())
        return _
        


    # @property
    # def fmap(self):
    #     """return the whole thing like a func""" 
    #   maybe put this in composition
    #     ...

# can this be reworked with python setters and getters?
    # def __repr__(self):
    #     # the arrow thing is for when this can be viewed as a 'function'
    #     name = self.name if self.name else self.__class__.__name__
    #     if self.name:
    #         _ = map(set, self.io)
    #         i,o = map(lambda _: '{}' if not _ else repr(_), _)
    #         _ = f"{name}({i}→{o})"
    #         return _
    #     else:
    #         return repr(super().__init__())
