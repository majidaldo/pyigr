from typing import Any, Self, Iterable
from .core import Node as _, Arrow

from kanren import run, var, Var
from kanren.constraints import neq
from kanren import eq, lall, lany
from kanren import Relation
from unification import unifiable


class Node(_):
    def __init__(self, node: Var | Self=None) -> None:
        self.node = node if node else var()
    
    def __hash__(self) -> int:
        return hash(self.node)

    def __gt__(self, other: Self) -> 'QuerySpec':
        return  QuerySpec(
                    Edge(self, other))
        
    def __repr__(self) -> str:
        return str(self.node)
    
    def __eq__(self, __value: Self) -> bool:
        return self.node == self.node
    
    def __invert__(self) -> 'Self':
        return self.__class__(var(self.node))

Arrow = unifiable(Arrow)


#from .core import Traversal. does traversal need to be in core?

from .core import Edge as _
class Edge(_):

    def __repr__(self) -> str:
        return f"{repr(self.s)}\u2192{repr(self.d)}"
    

class QuerySpec:
    def __init__(self, edge:Edge, exclude:bool = False ) -> None:
        self.edge = edge
        self.exclude = exclude
    
    def __repr__(self) -> str:
        return f"{'+' if not self.exclude else '-'}({self.edge})"
    
    def __neg__(self):
        return self.__class__(self.edge, not self.exclude)
    
    def __and__(self, other: Self | 'Query') -> 'Query':
        if isinstance(other, Query):
            return other & self
        else:
            assert(isinstance(other, self.__class__))
            return Query([self, other])


class Query:
    from kanren import var
    def __init__(self, specs:Iterable[QuerySpec] ) -> None:
        self.specs: list = specs if specs else []

    def __repr__(self) -> str:
        return '\n'.join(repr(s) for s in self)
    
    def relation(self, pg):
        pth = Relation()
        from networkx import all_simple_edge_paths
        for s,d in self:
            for p in all_simple_edge_paths(pg, s, d):
                ...
        pth.add_fact(*pg)
        return pth
    
    def vars(self):
        from itertools import chain
        return frozenset(chain.from_iterable(s.edge for s in self))

    def __call__(self, pg, n=None) -> Any:
        if n is None: n=0
        r = self.relation(pg)
        def unique(rs):
            ss = set()
            for r in rs:
                s = frozenset(r)
                if s in ss:
                    continue
                else:
                    ss.add(s)
                    yield r
        r = run(n, vars, r, 
                results_filter=unique)
        return r
        
    def __iter__(self) -> Iterable[Edge]:
        for s in self.specs: yield s

    def append(self, other: QuerySpec):
        self.specs.append(other)
    def __and__(self, other: QuerySpec) -> Self:
        _ = self.append(other)
        return self
    def extend(self, others: Iterable[QuerySpec]):
        self.specs.extend(others)


del _