# might be the boostrap to category theory
from turtle import rt
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
        def small(big): return {s:big[s] for s in smallset if s in bigset}
        return small


    @classmethod
    def partials(cls, vars: dict, lvldiff ={1,},  all=True):
        for ss1 in subsets(vars):
            for ss2 in subsets(vars):
                if not ss2.issubset(ss1): continue
                ss_big   = ss1
                ss_small = ss2
                if all: #                         if len(ssbig)==len(sssmall) this is id!
                    if len(ss_big)>len(ss_small):
                        yield       ss_big, ss_small#, lambda big: {s:big[s] for s in ss_small}
                else:
                    # just take 1 'level' diff
                    if (len(ss_big)-len(ss_small)) in lvldiff:
                        yield   ss_big, ss_small
    
    @staticmethod
    def combine(i, o): return i | o


def subsets(lst):
    from itertools import combinations
    for r in range(len(lst) + 1):
        for c in  (combinations(lst, r)):
            yield frozenset(c)



def varsafter(c: Connecting):
    _ = c.copy()
    def add():
        for fm in _.fmaps:
            io = set()
            io.update(*fm.i)
            io.update(*fm.o)
            io = types.Set(io)
            _.add_func(SetMap.combine, 
                {'i': types.Set(*fm.i),
                 'o': types.Set(*fm.o) ,
                'return': (io,) } )
    # oldn = len(_.fmaps)
    # newn = -1
    # while oldn != newn:
    #     add()
    #     newn = len(_.fmaps)
    add()
    return _

class Sets:
    def __init__(self, conn: Connecting):
        self._conn = conn
        self.conn = Connecting(name=f'Set({conn.name})' if conn.name else None)
        S = ctypes.Set  # to emphasize
        for fm in conn.fmaps:
            # sets -> sets
            self.conn.add_func(SetMap(fm), {'input': fm.i , 'return': (fm.o,) } ) # interesting...

    # def __repr__(self):     return repr(self.conn)
    # def _display_(self):    return self.conn._display_()

    from functools import cached_property

    @cached_property
    def partials(self)->Connecting:
        _ = Connecting()
        S = ctypes.Set
        # for fm in self.con.fmaps: vars the other way is to 'centralize' the subsetting with a unique function
        # but in the interest of a diagram, that would clutter.
            
        ss = set()
        for fm in self.conn.fmaps:
            ss.update(*(fm.i))
            ss.update(*(fm.o))
        for bigs, smls in SetMap.partials(ss):
            bigs2 = bigs
            smls2 = smls #  need to do this for some reason!!!!!!!!
            f = SetMap.big2small(bigs2, smls2)
            _.add_func(f, {'big': S(bigs), 'return': (S(smls2), )  } )
        return _

    @cached_property
    def all_paths(self):
        all_paths = Connecting()
        all_paths.add_conn(self.conn)
        all_paths.add_conn(self.partials)
        return all_paths

    from functools import cached_property
    #@property
    #def hom(self):
        ##return the set of funs below
    #    return self.paths
    # def hom or paths?
    @cached_property
    def hom(self):# -> Connecting:
        all_paths = self.all_paths

        varsets = set()
        for fm in all_paths.fmaps:
            varsets.add(*fm.i)
            varsets.add(*fm.o)
        del fm
        ifvarsets = set()
        ofvarsets = set()
        for fm in self.conn.fmaps:
            ifvarsets.add(*fm.i)
            ofvarsets.add(*fm.o)
        del fm

        from collections import defaultdict as dd
        hs = dd(dict)

        def find(s, d):
            ps = all_paths
            #from networkx import all_simple_edge_paths  # to more directly represent composition? it would look just like hom
            from networkx import all_simple_paths
            from ..connecting import Graph
            for p in all_simple_paths(ps.graph, s, d):
                _ = Connecting() # for each path or the set of paths?
                for n in p:
                    if ps.graph.nodes[n][Graph.terms.types.type] == Graph.terms.types.f.function:
                        #yield n
                        _.add_fmap(n)
                        yield _
        return find
        #c = Connecting()
        for i in ifvarsets:
            for o in ofvarsets:
                #c.add_func(lambda input: _, {'input': s, 'return': (d,) }  )
                _ = find(i,o)
                hs[i][o] = types.Set(_) 
        # put id? TODO
        return hs
        
