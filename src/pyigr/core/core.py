from typing import (
    # function 
    Any, Callable, Annotated,
    # node stuff
    Hashable,
    # mapping
    Iterable, Tuple, Mapping,
    # g
    Literal, Dict,
    # 
    Self
)

class Node(Hashable):...

class Morphism(Callable): ...
    
_tuple = tuple
class tuple(_tuple):
    def __repr__(self) -> str:
        _ = (repr(e).strip("'") for e in self)
        return f"({','.join(_)})"
del _tuple
_frozenset = frozenset
class frozenset(_frozenset):
    def __repr__(self) -> str:
        _ = (repr(e).strip("'") for e in self)
        return f"{{{','.join(_)}}}"
del _frozenset

from inspect import signature
import networkx as nx


Src, Dst = [Node]*2  # i'm this lazy
#Edge = Tuple[Src, Dst]
from typing import NamedTuple
class Edge(NamedTuple):
    s: Src
    d: Dst
# too strict. just use callable
Arrow = Tuple[Src, Morphism, Dst] # src and dst are 'one thing'
class Arrow(NamedTuple):
    s: Src
    f: Callable[[Src], Dst]
    d: Dst
    # def __new__(cls, s, f, d):
    #     if not isinstance(f, Morphism):
    #         f = Morphism(f)
    #     _ = super().__new__(cls, s, f, d)
    #     _.__init__((s, f, d))
    #     return _

    @property
    def m(self): return self.f
    def __repr__(self):
        return f"{fnamer(self.f)}:{self.s}\u2192{self.d}"
    def __gt__(self, other: 'Arrow | None'):
        # put it in a C to check?
        if self.d == other.s:
            #                            might as well just do it in the graph
            return self.__class__(self.s, self.f > other.f  , other.d)
        # raise?
# ...or user could put them in as identities
# looking for the 'primitive'.
#Traversal = Tuple[Morphism] # st t1.dst = t2.src. but you can't say this in python


#TMap = Mapping[Traversal, Traversal]
#NMap = Mapping[Src, Dst]
# can get the above from below?
FMap = Mapping[Arrow, Arrow]
# this should be it!!

class types:
    edge = Tuple[Edge, Dict[Literal['f'], Arrow.f]]
types = types()
class G(nx.MultiDiGraph):
    types = types

    def __iter__(self):
        for s,d,f in self.edges(keys=True):
            yield Arrow(s,d,f)
del types

from typing import TypeVar
IDType = TypeVar('IDType')
class id(Morphism): # dont care for the python builtin id. but reprs are fine.
    def __call__(self, one: IDType) -> IDType:
        return one
    def __repr__(self) -> str:
        return 'id'
    def __str__(self) -> str:
        return 'id'
id = id()

fnamer = lambda f: f"{f.__module__+'.' if f.__module__ != '__main__' else ''}{f.__name__}"


class PG:
    value_key = 'value'
    
    @classmethod
    def get_new_list(cls, maxlen=100):
        if maxlen:
            from collections import deque
            return deque(maxlen=100)
        else:
            return list()

    def __init__(self) -> None:
        def _():
            i = 0
            while True:
                yield i
                i = i+1
        self.nodegen: Iterable[int] = _()
        self.fg = G()
        self.default_repr: Literal['listing']|Literal['table'] = 'listing'

    @property
    def repr(self,):
        def table():
            g = self.fg
            from rich.table import Table
            _ = Table(title=self.name)
            _.add_column(r'o\m')
            ms = (e[-1] for e in g.edges(data='f')) # (a.f for a in self)
            ms = frozenset(ms)
            ms = list(ms)
            for m in ms:
                _.add_column(repr(m))
            for s in g.nodes:#:frozenset(a.s for a in self):
                def fd():
                    for d,_f in g[s].items():
                        for i,ad in _f.items():
                            yield ad['f'],d
                f2d = dict(fd())
                _.add_row(
                    # why need to strip?
                    repr(s).strip("'"),
                    *(repr(f2d[m]).strip("'") if m in f2d else ''  for m in ms))
            return _
        
        # only repr id if all arrows are self
        if frozenset(a.f for a in self) == frozenset( (id,) ):
            listing = lambda: '\n'.join(map(repr, (a for a in self   ) ) )
        else:
            listing = lambda: '\n'.join(map(repr, (a for a in self if a.f!=id  ) ) )
        from types import SimpleNamespace as NS
        return NS(
            listing=listing,
            table=table,
            self=lambda: self.name)
    def __repr__(self) -> str:
        return getattr(self.repr, self.default_repr)()

    def __match_args__(self):
        raise NotImplementedError
    
    def g(self, namer: Callable[Callable, str]=fnamer):
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
    
    def __iter__(self,) -> Iterable[Arrow]:
        for e in self.fg.edges(keys=True):
            yield Arrow(e[0], e[2] , e[1])
    
    def keys(self, ) -> Iterable[Node]:
        yield from self.fg.nodes
    @property
    def nodes(self):
        yield from self.keys()
    
    def __getitem__(self, node: Node) -> list[Any]:
        if node == (): return ()
        if self.value_key not in self.fg.nodes[node]:
            self.fg.nodes[node][self.value_key] = self.get_new_list()
        return self.fg.nodes[node][self.value_key]#[-1] # the last one
    def __setitem__(self, node: None, value: Any) -> None:
        if node == (): raise KeyError(f'cannot put value in ()')
        if  self[node] is None:
            l = self.get_new_list()
            l.append(value)
            self.fg.nodes[node][self.value_key] = l
        else:
            self.fg.nodes[node][self.value_key].append(value)
    def values(self):
        for n in self.nodes: yield self[n]
    
    def __call__(self, ms: Iterable[Arrow]) -> Any:
        # exciting things!! jiting/compilation, parallelization.
        # add to 'returns' list
        for m in ms:
            # get value
            _ = self[m.s][-1] if self[m.s] != () else ()
            # process
            _ = m.f(*_) if isinstance(_, tuple) else m.f(_)
            # put
            self[m.d].append(_)

    def add_morphism(self, m: Arrow) -> None | G.types.edge:
        m = Arrow(*m) if not isinstance(m, Arrow) else m
        assert(isinstance(m, Arrow))
        e = Edge(m.s, m.d)
        p, k=  (e, {'key':m.f})
        self.fg.add_edge(*p, **k)
        return p,k

    # SETTING stuff
    def add_f(self, f: Callable) -> Tuple[Arrow]:
        sig = signature(f)
        if (sig.return_annotation is sig.empty) or (not isinstance(sig.return_annotation, type(Annotated[Any,''])  )  ):
            dst = next(self.nodegen)
        else:
            dst = sig.return_annotation.__metadata__[0] # just take the first thing: Annotated[type, 0, 1, ... ]
        r = []
        def am(s,f,d): # (a)dd(m)eta
            r.append(
                self.add_morphism(
                    Arrow(s,f,d)))
        
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
            src = srcs[0][0] # idk
            am(src, f, dst,)
        elif len(srcs) == 0:
            src = ()
            am(src, f, dst)
        else:
            def _gs(t, i):
                def selector(*t):
                    return t[i]
                return selector
            # make a tuple node
            srcs = tuple(s[0] for s in srcs)
            am(srcs, f, dst)
            # then getters tpl->elem
            for i, p in enumerate(srcs):
                am(srcs, _gs(srcs, i) , p[0])
            
        return tuple(r) if r[0] is not None else None


    def query(self, q: 'str | expr' ):
        ...

    #def add_structure ( data : dict[dict[callable ]] )
    
    # def > op to set stuff

    # EXE


    # MAPPING to other world stuff

    # self, 
    # exec map


    # interesting:
    # for CT: def equations.

    




