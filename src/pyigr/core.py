from typing import (
    # function 
    Any, Callable, Annotated,
    # node stuff
    Hashable,
    # mapping
    Iterable, Tuple, Mapping,
    # g
    Literal, Dict
)
from inspect import signature

import networkx as nx


Src, Dst = [Hashable]*2  # i'm this lazy
#Edge = Tuple[Src, Dst]
from typing import NamedTuple
class Edge(NamedTuple):
    s: Src
    d: Dst
# too strict. just use callable
Morphism = Tuple[Src, Callable, Dst] # src and dst are 'one thing'
class Morphism(NamedTuple):
    s: Src
    f: Callable[[Src], Dst]
    d: Dst
# ...or user could put them in as identities
# looking for the 'primitive'.
#Traversal = Tuple[Morphism] # st t1.dst = t2.src. but you can't say this in python
class Traversal(Tuple[Morphism]):
    def __init__(self, ms: Iterable[Morphism]) -> None:
        super().__init__()
        ms = tuple(ms)
        for m1, m2 in zip(ms, ms[1:]):
            if (m1.dst != m2.src):
                raise ValueError("not a path")
    
    # def sort


#TMap = Mapping[Traversal, Traversal]
#NMap = Mapping[Src, Dst]
# can get the above from below?
FMap = Mapping[Morphism, Morphism]
# this should be it!!

class types:
    edge = Tuple[Edge, Dict[Literal['f'], Morphism.f]]
types = types()
class G(nx.MultiDiGraph):
    types = types

    def __iter__(self):
        for s,d,f in self.edges(keys=True):
            yield Morphism(s,d,f)
del types

from typing import TypeVar
IDType = TypeVar('IDType')
class identity:
    def __call__(self, one: IDType) -> IDType: 
        return one
    def __repr__(self) -> str:
        return 'id'
    def __str__(self) -> str:
        return 'id'
identity = identity()

fnamer = lambda f: f"{f.__module__+'.' if f.__module__ != '__main__' else ''}{f.__name__}"
def _tuplegetter(t, i):
    def tuplegetter(i):
        return t[i]
    return tuplegetter

class PG:

    def __init__(self) -> None:
        def _():
            i = 0
            while True:
                yield i
                i = i+1
        self.nodegen: Iterable[int] = _()
        self.fg = G()
    
    def g(self, namer:Callable[Callable, str]=fnamer):
        "'nice' graph"
        g = G()
        for m in self:
            g.add_edge(m.s, m.d, namer(m.f) )
        # gets a function name and values
        return g
    
    def structure_hash(self):
        # where the node labels don't matter.
        # some isomorphism thing
        ...
    def value_hash(self):
        ...
    
    def __iter__(self,) -> Iterable[Morphism]:
        for e in self.fg.edges(keys=True):
            yield Morphism(e[0], e[2] , e[1])
    # def __getitem__(self, k: Callable | Tuple[Hashable, Hashable] | Mapping ) -> Iterable:
    #     #
    #     # could be a dict or data to create pure structure?
    def __getitem__(self, k):
        return self.fg
    def __setitem__(self, k):
        return self.fg
    
    def __call__(self, ms: Iterable[Morphism]) -> Any:
        # exciting things!! jiting/compilation, parallelization.
        # add to 'returns' list
        v = 'v'
        for m in ms:
            # get
            _ = self.nodes[m.s][v]
            # process
            _ = m.f(*_)
            # put
            self.nodes[m.d][v] = _

    def add_morphism(self, m: Morphism) -> None | G.types.edge:
        m = Morphism(*m) if not isinstance(m, Morphism) else m
        assert(isinstance(m, Morphism))
        e = Edge(m.s, m.d)
        # why not work?!
        #m.f.__repr__ = lambda slf: f"{sxxlf.__module__}.{self.__name__}"
        p, k=  (e, {'key':m.f})
        if (e.s in self.fg.nodes) and (e.d in self.fg.nodes):
            if m.f not in self.fg.nodes[e.s][e.d]:
                self.fg.add_edge(*p, **k)
                return p, k
        else:
            self.fg.add_edge(*p, **k)
            return p, k

    # SETTING stuff
    def add_f(self, f: Callable) -> Tuple[Morphism]:
        sig = signature(f)
        if (sig.return_annotation is sig.empty) or (not isinstance(sig.return_annotation, Annotated)  ):
            dst = next(self.nodegen)
        else:
            dst = sig.return_annotation.__metadata__
        r = []
        def am(s,f,d):
            r.append(
                self.add_morphism(
                    Morphism(s,f,d)))
        
        srcs = []
        for p in sig.parameters.values():
            if p.annotation is sig.empty:
                src = next(self.nodegen)
            else:
                src = p.annotation.__metadata__
            del p
            srcs.append(src)
        srcs = tuple(srcs)
        
        if len(srcs) == 1:
            src = srcs[0]
            am(src, f, dst,)
        else:
            # make a tuple node
            tn = str(srcs)
            am(tn, f, dst)
            # then getters tpl->elem
            for i, p in enumerate(srcs):
                am(p[0], _tuplegetter(srcs, i) , tn)
            
        return tuple(r)

    #def add_structure ( data : dict[dict[callable ]] )
    
    # def > op to set stuff

    # EXE


    # MAPPING to other world stuff

    # self, 
    # exec map


    # interesting:
    # for CT: def equations.



