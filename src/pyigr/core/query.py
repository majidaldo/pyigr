from typing import Self, Iterable, Tuple
from .core import Node as _, Arrow

from kanren import run, var, Var
from kanren import eq
from kanren.constraints import neq
from kanren import Relation
from unification import unifiable

class Node(_):
    def __init__(self, node: Var | _ =None) -> None:
        self.node = node if node is not None else var()

    @property
    def isvar(self):
        if isinstance(self.node, Var):
            return True
        if isinstance(self.node, tuple):
            return all(isinstance(e, Var) for e in self.node)
        return False
    
    def __hash__(self) -> int:
        return hash(self.node)

    def __gt__(self, other: Self) -> 'QuerySpec':
        return  QuerySpec(
                    Edge(self, other))
        
    def __repr__(self) -> str:
        return str(self.node)
    
    def __eq__(self, other: Self) -> bool:
        if isinstance(other, self.__class__):
            return self.node == other.node
        else:
            return self.node == other
    
    def __invert__(self) -> 'Self':
        if isinstance(self.node, tuple):
            return self.__class__(tuple(var(e) for e in self.node))
        else:
            return self.__class__(var(self.node))
            


Arrow = unifiable(Arrow)


from functools import cached_property

@unifiable
class Traversal(Tuple[Arrow]): 
    # "path" doesn't imply execution.
    def __init__(self, ms: Iterable[Arrow]) -> None:
        super().__init__()
        ms = tuple(ms)
        for m1, m2 in zip(ms, ms[1:]):
            if (m1.d != m2.s):
                raise ValueError("not a path")
            
    @property
    def s(self): return self[0].s
    @cached_property
    def composition(self):
        return tuple(_.f for _ in self)
    @property
    def d(self): return self[-1].d
    
    def __repr__(self) -> str:
        from .core import fnamer
        ft = '\u25e6'.join(map(lambda a:fnamer(a.f), reversed(self)))
        return f"{ft}:{self[0].s}\u2192{self[-1].d}"


from .core import Edge as _
class Edge(_):

    def __repr__(self) -> str:
        return f"{repr(self.s)}\u2192{repr(self.d)}"
    

class QuerySpec:
    def __init__(self, edge:Edge,  ) -> None:
        self.edge = edge
    
    def __repr__(self) -> str:
        return str(self.edge)
    
    def __and__(self, other: Self | 'Query') -> 'Query':
        if isinstance(other, Query):
            return other & self
        else:
            assert(isinstance(other, self.__class__))
            return Query([self, other])
    
    @property
    def query(self) -> 'Query':
        return Query([self])


class Query:
    from kanren import var
    def __init__(self, specs:Iterable[QuerySpec] ) -> None:
        self.specs: list = specs if specs else []

    @classmethod
    def parse(cls, s: str) -> Self:
        # parse s to queryspecs
        raise NotImplementedError

    def __repr__(self) -> str:
        return '\n'.join(repr(s) for s in self)
    
    def paths(self, pg):
        pg = pg.fg
        r = Relation()
        from networkx import all_simple_edge_paths
        def p2t(p):
            t = Traversal(Arrow(s, f, d) for s,d,f in p)
            return t.s, t, t.d

        for qs in self:
            if not qs.edge.s.isvar:
                if qs.edge.s.node not in pg:
                    continue
            if not qs.edge.d.isvar:
                if qs.edge.d.node not in pg:
                    continue

            if not qs.edge.s.isvar and not qs.edge.d.isvar:
                for pth in all_simple_edge_paths(pg, qs.edge.s.node, qs.edge.d.node):
                    r.add_fact(*p2t(pth))
            else:
                if qs.edge.s.isvar:
                    s = pg.nodes
                else:
                    s = [qs.edge.s]
                if qs.edge.d.isvar:
                    d = pg.nodes
                else:
                    d = [qs.edge.d]
                from itertools import product
                for s,d in product(s,d):
                    for pth in all_simple_edge_paths(pg, s, d):
                        r.add_fact(*p2t(pth))
        return r
    
    def vars(self):
        from itertools import chain
        return frozenset(chain.from_iterable(s.edge for s in self))

    def __call__(self, pg, n=None) -> Iterable[Traversal]:
        if n is None: n=0
        r = self.paths(pg)
        def unique(rs):
            ss = set()
            for r in rs:
                s = frozenset(r)
                if s in ss:
                    continue
                else:
                    ss.add(s)
                    yield r
        inc = (tuple((qs.edge.s.node, var() , qs.edge.d.node)) for qs in self )
        inc = tuple(inc)
        r = run(n,
                tuple(i[1] for i in inc),
                *(r(i[0], i[1], i[2]) for i in inc),
                #*(neq(c[0], c[1]) for c in vpairs ),
                #results_filter=unique
        )
        #r = (Traversal(t) for t in r)
        return r
        
    def __iter__(self) -> Iterable[QuerySpec]:
        for s in self.specs: yield s

    def append(self, other: QuerySpec):
        self.specs.append(other)
    def __and__(self, other: QuerySpec) -> Self:
        _ = self.append(other)
        return self
    def extend(self, others: Iterable[QuerySpec]):
        self.specs.extend(others)


del _