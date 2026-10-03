# might be the boostrap to category theory
try: from icecream import ic
except ImportError: pass

def dataclass(c):
    from dataclasses import dataclass
    return dataclass(frozen=True)(c)


from ..connecting import Connecting, types as ctypes, FMap
from .composition import id
class types:
    Set = ctypes.Set

class SetMap: 
    """
    'converts' what was established in Connecting
    to just mappings from sets to sets.
    """
    def __init__(self, fm: FMap):
        self.fm = fm
    def __repr__(self):
        return '*'+repr(self.fm)

    def __call__(self, input: dict) -> dict:
        return self.fm(input)

    @staticmethod
    def big2small(bigset, smallset):
        return lambda big: {s:big[s] for s in smallset if s in bigset}

    @classmethod
    def partials(cls, vars: dict, all=False):
        for ss1 in subsets(vars):
            for ss2 in subsets(vars):
                if len(ss1)>=len(ss2): # too many.
                    if not ss2.issubset(ss1): continue
                    ss_big   = ss1
                    ss_small = ss2
                    if all: #                         if len(ssbig)==len(sssmall) this is id!
                        yield       ss_big, ss_small#, lambda big: {s:big[s] for s in ss_small}
                    else:
                        # just take 1 'level' diff
                        if (len(ss_big)-len(ss_small)) in {1,}:#0}:
                            yield   ss_big, ss_small


def subsets(lst):
    from itertools import combinations
    for r in range(len(lst) + 1):
        for c in  (combinations(lst, r)):
            yield frozenset(c)


class Sets:#(FMap or Connecting) make it look like FMap or Connecting? 
    def __init__(self, conn: Connecting):
        self.conn = Connecting(name=f'Set({conn.name})' if conn.name else None)
        S = ctypes.Set  # to emphasize
        for fm in conn.fmaps:
            # sets -> sets
            self.conn.add_func(SetMap(fm), {'input': fm.i , 'return': (fm.o,) } ) # interesting...
            #self.con.add_func(id, {'i': (fm.i), 'return': ((fm.i),) } ) # # interesting nesting
            #self.con.add_func(id, {'i': (fm.o), 'return': ((fm.o),) } ) # 
            #for i in fm.i: self.con.add_func(id)
            #for o in fm.o: self.con.add_func(id)
    def x__init__(self, conn: Connecting):
        self.conn = conn

    # def __repr__(self):     return repr(self.conn)
    # def _display_(self):    return self.conn._display_()

    from functools import cached_property
    @cached_property
    def partials(self)->Connecting:
        _ = Connecting()
        S = ctypes.Set
        # for fm in self.con.fmaps: vars the other way is to 'centralize' the subsetting with a unique function
        # but in the interest of a diagram, that would clutter.
        iz, oz = [], []
        for fm in self.conn.fmaps:
            iz.extend(*fm.i)
            oz.extend(*fm.o)
        for bigs, smls in SetMap.partials(set(iz)|set(oz)):
            bigs2 = bigs
            smls2 = smls #  need to do this for some reason!!!!!!!!
            f = SetMap.big2small(bigs2, smls2)
            _.add_func(f, {'big': S(bigs), 'return': (S(smls2), )  } )
        return _

    from functools import cached_property
    @cached_property
    def hom(self):# -> Connecting:
        def _():
            for fm in self.con.fmaps:
                yield fm.i, fm.o

        self.conn.add(self.partials)
        _ = self.conn
        #from networkx import all_simple_edge_paths  # to more directly represent composition? it would look just like hom
        #from networkx import all_simple_paths
        #_ = all_simple_paths(self.con.graph, self.con.fmaps[0], self.con.fmaps[2],)
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
