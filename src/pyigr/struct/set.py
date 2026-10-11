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
    

    @classmethod
    def big2small(cls, bigset, smallset):
        def big2small(big): return {s:big[s] for s in smallset if s in bigset}
        return big2small


    @classmethod
    def subsets(cls, vars: dict, lvldiff ={1,0},  all=False, id=False):
        for ss1 in subsets(vars):
            for ss2 in subsets(vars):
                if not ss2.issubset(ss1): continue
                ss_big   = ss1
                ss_small = ss2
                if not id:
                    if ss_big == ss_small: continue
                if all: #                         if len(ssbig)==len(sssmall) this is id!
                    if len(ss_big)>len(ss_small):
                        yield       ss_big, ss_small#, lambda big: {s:big[s] for s in ss_small}
                else:
                    # just take 1 'level' diff
                    if (len(ss_big)-len(ss_small)) in lvldiff:
                        yield   ss_big, ss_small
    
    @classmethod
    def small2big(cls, l, r): return l | r

    @classmethod
    def fio(cls, input, f,):
        def fio(input):
            _ = cls.small2big(input, f.f(input), )
            return _
        return fio


def subsets(lst):
    from itertools import combinations
    for r in range(len(lst) + 1):
        for c in  (combinations(lst, r)):
            yield frozenset(c)


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

    
    def varpaths(self) -> dict:
        from collections import defaultdict as dd
        #_ = dd(list) #does not work like this!
        #paths = dd(lambda: _)
        paths = dd(lambda: dd(set))

        iz,oz = set(), set()
        for fm in self._conn.fmaps:
            iz.update(fm.i)
            oz.update(fm.o)
        for i in iz|oz:
            for o in iz|oz:
                paths[i][o] # init
        for i in iz:
            for o in oz:
                for p in find_paths(self._conn, i, o):
                    paths[i][o].add(p)
        # list just for nice display in marimo
        for i in paths:
            for o in paths[i]:
                #paths[i][o] = list(((paths[i][o]))) #  why the *FUCK* is this not unique?!?!
                paths[i][o] = list(frozenset(list(frozenset(paths[i][o])))) # why the *FUCK* do i have to do it a couple times!!!!
                
        # convert to regular dict so no new items get created on access
        paths = dict(paths)
        paths = {i:dict(o) for i,o in paths.items()}
        return paths
    
    from functools import cached_property
    @cached_property
    def fmpaths(self):
        # capture {i}(f compositions){o}: [{i}][{o}]
        vps = self.varpaths()
        for i in vps:
            for o in vps[i]:
                ps = vps[i][o]
                vps[i][o] = []
                for p in ps:
                    # accumulations
                    l = []
                    for ifm in range(1,len(p.fmaps)+1):
                        _ = Connecting()
                        for fm in p.fmaps[:ifm]:
                            _.add_fmap(fm)
                        l.append(_)
                    vps[i][o].append(l)
        return vps
    

    @cached_property
    def paths(self):# -> Connecting:
        from collections import defaultdict as dd
        hs = dd(lambda: dd(set))
        fmps = self.fmpaths
        for i in fmps:
            for o in fmps[i]:
                for cons in fmps[i][o]:
                    for c in cons:
                        hs[c.i][c.o].add(c)
        for i in hs:
            for o in hs[i]:
                hs[i][o] = list(frozenset(list(hs[i][o])))
        # put id? TODO
        hs = dict(hs) # dont want dd out.
        return hs
        

def find_paths(c: Connecting, s, d,):
    #from networkx import all_simple_edge_paths  # to more directly represent composition? it would look just like hom
    from networkx import all_simple_paths
    #from networkx import shortest_path
    from ..connecting import Graph
    #for p in [shortest_path(ps.graph, s, d)]:
    for p in all_simple_paths(c.graph, s, d):
        _ = Connecting() # for each path or the set of paths?
        for n in p:
            if c.graph.nodes[n][Graph.terms.types.type] == Graph.terms.types.f.function:
                #yield n
                _.add_fmap(n)
                yield _
