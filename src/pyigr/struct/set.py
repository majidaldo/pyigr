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
    def dictin(input: dict):
        s = types.Set(input.keys())
        _ = {s: input}
        return _

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


class Sets:
    def __init__(self, conn: Connecting):
        self.conn = Connecting(name=f'Set({conn.name})' if conn.name else None)
        S = ctypes.Set  # to emphasize
        for fm in conn.fmaps:
            # sets -> sets
            self.conn.add_func(SetMap(fm), {'input': fm.i , 'return': (fm.o,) } ) # interesting...

    # def __repr__(self):     return repr(self.conn)
    # def _display_(self):    return self.conn._display_()

    from functools import cached_property
    @cached_property
    def paths(self)->Connecting:
        # functions  + partials in the same 'substrate' (to make it easier for .paths)
        _ = Connecting()
        S = ctypes.Set
        # for fm in self.con.fmaps: vars the other way is to 'centralize' the subsetting with a unique function
        # but in the interest of a diagram, that would clutter.
        iz, oz = set(), set()
        for fm in self.conn.fmaps:
            iz.update(*(fm.i))
            oz.update(*(fm.o))
        for bigs, smls in SetMap.partials(set(iz)|set(oz)):
            bigs2 = bigs
            smls2 = smls #  need to do this for some reason!!!!!!!!
            f = SetMap.big2small(bigs2, smls2)
            _.add_func(f, {'big': S(bigs), 'return': (S(smls2), )  } )
        self.conn.add(_)
        _ = self.conn
        return _

    from functools import cached_property
    #@property
    #def hom(self):
        ##return the set of funs below
    #    return self.paths
    # def hom or paths?
    @cached_property
    def hom(self):# -> Connecting:
        ps = self.paths
        varsets = set()
        for fm in ps.fmaps:
            varsets.add(*fm.i)
            varsets.add(*fm.o)
        del fm
        from collections import defaultdict as dd
        hs = dd(dict)

        def find(s, d):
            #from networkx import all_simple_edge_paths  # to more directly represent composition? it would look just like hom
            from networkx import all_simple_paths
            _ = Connecting() # not for each path?
            from ..connecting import Graph
            for p in all_simple_paths(ps.graph, s, d):
                for n in p:
                    if ps.graph.nodes[n][Graph.terms.types.type] == Graph.terms.types.f.function:
                        #yield n
                        _.add_fmap(n)
                        yield _
            return _
        
        #c = Connecting()
        for s in varsets:
            for d in varsets:
                _ = find(s,d)
                #c.add_func(lambda input: _, {'input': s, 'return': (d,) }  )
                hs[s][d] = types.Set(find(s,d)) 
        # put id? TODO
        return hs
        

