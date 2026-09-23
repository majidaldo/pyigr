try:
    from icecream import ic
except ImportError: pass

# this seems like a 'low' level primitive
# (to build on)
# it just deals with connectivity
from typing import Any, Self, Callable, Iterable, Hashable, Literal
def dataclass(c):
    from dataclasses import dataclass
    return dataclass(frozen=True)(c)

class types:
    var_key = Hashable
    type kw = str
    type arg = kw | int
    returnkey = Literal['return']
    from typing import get_args
    returnkeyvalue = get_args(returnkey)[0]
    multioutkeys =  frozenset
    argmap = dict[arg, var_key] 
    iomap = dict[arg | returnkey, var_key | multioutkeys]
    del get_args


    class IO(frozenset):
        def __repr__(self):
            _ = (io for io in self)
            _ = map(repr, _)
            _ = sorted(_, key=str)
            _ = map(lambda _: _.replace('"', '').replace("'", '' ) , _)
            _ = ','.join(_)
            return _

    class IOMap(iomap):
        # should not change.
        # lives in FMap(frozen)
        def __hash__(self):
            return hash(tuple(sorted(self.items())))
        
        def __repr__(self):
            def io(i,o):
                _ = map(str, (i,o))
                _ = map(lambda _: _.replace('"', '').replace("'", ''), _)
                i,o = _
                _ = f"{i}→{o}"
                return _
            rk = types.returnkeyvalue
            iz = {k:v for k,v in self.items() if k!=rk}
            oz = {o  for o in self[rk]}
            iz = '\n'.join(io(k,    v) for (k,v) in  iz.items())
            oz = '\n'.join(io('',   o) for o in  oz)
            return '\n'.join((iz,oz))


@dataclass
class FMap:
    # use wrapt?
    """
    reresents mapping from vars/state to f
    """
    m: types.iomap
    from typing import Callable
    i: frozenset
    f: Callable
    o: frozenset

    from functools import cached_property
    @cached_property
    def tuple(self):
        # i and o are determinded by fmap
        # so the following is unique (i think!)
        # and hopefull convenient as a key
        return (self.i, self.f, self.o)
    @classmethod
    def from_tuple(cls, i, f, o):
        return cls(i=i,f=f,o=o)

    @classmethod
    def from_iomap(cls, f, fmap: types.iomap):
        from typing import get_args
        returnkey  : types.returnkey = get_args(types.returnkey)[0]
        if returnkey not in fmap:
            raise AssertionError(f"{returnkey} not in fmap.")
        from inspect import signature 
        sig = signature(f)
        argmap = {k:v for k,v in fmap.items() if k != returnkey}
        argmap = cls.kwargmap(f, tuple(argmap.items()))
        # just try to, to raise exception if issue
        sig.bind(**{a:None for a in argmap })
        if isinstance(fmap[returnkey], Iterable):
            returns = fmap[returnkey]
        else:
            returns = {fmap[returnkey], }
        return cls(
            m = types.IOMap({**argmap, **{returnkey: frozenset(returns) }}),
            i=frozenset(argmap.values()),
            f=f,
            o=frozenset(returns),
            )


    from functools import cache
    from inspect import Signature
    @staticmethod         
    @cache                  # tuple so it can be cached
    def kwargmap(f, argmap: tuple[types.args, types.var_key], inv=False) -> dict[types.kw, types.var_key] | dict[types.var_key, types.kw] :
        """
        replace positionally placed args with keywords as a 'normalization'
        """
        argmap = dict(argmap)
        from inspect import signature
        sig = signature(f)
        for i, p in enumerate(sig.parameters): # ordered ok?
            if (i in argmap) and (p in argmap):
                raise KeyError(f'conflicting arguments: positional {i} and keyword {p} refer to the same argument.')
            else: # make everything kw
                try:
                    if p not in argmap:
                        argmap[p] = argmap[i]
                    if i in argmap:
                        argmap.pop(i)
                except KeyError: pass
                    
        for a in argmap:
            if isinstance(a, int):
                raise KeyError(f'positional argument {a} is not mapped.')
        # to make sure of the ordering
        argmap = {p:argmap[p] for p in  (sig.parameters) if p in argmap }
        if inv: argmap = {v:k for k,v in argmap.items()}
        return argmap


    def __post_init__(self):
        # sorting to make order not matter (does that make sense?!)
        object.__setattr__(self, 'i', types.IO(sorted(self.i, key=str)))
        object.__setattr__(self, 'o', types.IO(sorted(self.o, key=str)))

    def __repr__(self) -> str:
        i, o = map(lambda _: '{}' if not _ else '{'+repr(_)+'}' , (self.i, self.o))
        _ = f"{self.fname}:{i}→{o}"
        return _


    @cached_property
    def fname(self):
        f = self.f
        _ = repr(f)
        _ = _.strip('"').strip("'")
        if _.startswith('<') and _.endswith('>'):
            mod = (f"{f.__module__}.") if (f.__module__ != '__main__') else ''
            _ = f"{mod}{f.__name__}"
            return _
        else:
            return _
    @cached_property
    def __name__(self): return self.f.__name__
    @cached_property
    def __module__(self):   return self.f.__module__
    
    @cached_property
    def parameters(self):
        from inspect import signature
        return signature(self.f).parameters
    # cannot set another name for cached_property
    # params = parameters
    @cached_property 
    def params(self): return self.parameters
    from functools import cached_property
    @cached_property
    def signature(self):
        from inspect import signature
        return signature(self.f)
    @cached_property
    def sig(self): return self.signature
    @cached_property
    def bind(self): return self.sig.bind

    
    # application
    
    @cached_property
    def argmap(self) -> types.argmap:
        _ = {k:v for k,v in self.m.items() if k != types.returnkeyvalue}
        return _

    def __call__(self, values: dict[types.var_key, Any]):
        _ = self.argmap
        _ = tuple(_.items())
        _ = self.kwargmap(self.f, _)
        # user can check if argmap values are in values
        _ = {kw:values[k] for kw, k in _.items()}
        _ = self.bind(**_)
        return self.f(*_.args, **_.kwargs) # here _.kwargs are kw-only

    def returns(self, r: dict | Any) -> dict: # an update
        # 'regular' f o
        if len(self.o) == 1:
            (o, ) = self.o
            return {o: r}
        # output goes to all keys
        if not isinstance(r, dict):
            return {o:r for o in self.o}
        else:
        # outputs should map
            assert(isinstance(r, dict))
            r: dict
            # ...creating another dict but it's a safety?
            return {o:r[o] for o in self.o}

    from networkx import DiGraph
    def graph(self) -> DiGraph:
        from networkx import DiGraph
        g = DiGraph()
        terms = Graph.terms
        label = Graph.terms.label
        type = terms.types.type
        # INPUT outside in
        for farg,var in self.argmap.items():
            # outside->in
            farg = Graph.FArg(self.f, farg)
            g.add_node(var,             **{type: terms.types.variable.  variable,   label:str(var) })
            g.add_node(farg,            **{type: terms.types.f.         arg,        label:str(farg) })
            g.add_edge(var, farg,   **{type: terms.types.f.         binding.input     })
            del farg, var
        # F
        g.add_node(self,                **{type :terms.types.f.         function,   label:str(self.fname)})
        # OUTPUT in to outside
        for o in self.o:
            g.add_edge(self, o,     **{type: terms.types.f.binding. output })
            g.add_node(o,               **{type: terms.types.variable.  variable,   label:str(o) })
            del o
        return g

    # for composition ops you'd have to create unique intermediate/non-interacting vars

class Connect:
    def __init__(self,
            fmaps: Iterable[FMap] =[],
            name = None,):
        for fm in fmaps:
            self.add_func(fm)
        self.ops = []
        self._graph = Graph(self, name=name)
        self.graph = self._graph.graph
        self.name= name
    
    def __repr__(self):
        _ = (self.name+':') if self.name else ''
        _ = (_+'\n' if _ else _) + '\n'.join(map(repr, self.funcs))
        return _

    def _add_op(self, g):
        self.ops.append(g)

    def add_func(self, f, fmap: types.iomap = {}):
        from typing import get_args
        returnkey  : types.returnkey = get_args(types.returnkey)[0]
        from inspect import signature
        sig = signature(f)
        if returnkey not in fmap:
            returns = FMap.from_iomap(f, {**{p:p for p in sig.parameters}, **{returnkey: ''}}).fname
            returns = returns + str(len(self.funcs))
        else:
            returns = fmap[returnkey]
        argmap = {
            n:n if n not in fmap 
                else fmap[n] for n,p in sig.parameters.items()
                    if ((p.default) == p.empty) }
        fmap = {**argmap, **{returnkey: returns}}
        fm = FMap.from_iomap(f, fmap)
        g = fm.graph()
        self._graph.add_F(fm)
        self._add_op(g)
        return fm
    register_func = add_func

    @property
    def funcs(self):
        # i think same as insertion order
        def _():
            for n in self.graph.nodes:
                if self.graph.nodes[n][Graph.terms.types.type] == Graph.terms.types.f.function:
                    yield n
        return list(_())

    def register(self, fmap: types.argmap = {}, ):
        """decorator """ 
        if callable(fmap): # case when no (parens) used @register
            f = fmap
            argmap = {} # the default
            self.add_func(f)
            return f
        else:
            def decorator(f, fmap=fmap):
                self.add_func(f, fmap=fmap)
                return f
            return decorator

    def __add__(self, other: Self): return self.add(other)
    def add(self, other): # TODO
        # to get a new one
        from copy import deepcopy as copy
        new = copy(self)
        new.ops = []# clear this though
        self._add_op(self.add, other=other)
        return new
    

class Graph:
    class terms:
        class types:
            type =  'type'
            class f:
                function = 'function'
                i = 'i'  # func idx
                arg =   'arg'
                class binding:
                    binding = 'binding'
                    input = 'input'
                    output = 'output'
            class variable:
                variable =  'variable'
        value = 'value'
        label = 'label' # TODO
    @dataclass
    class FArg:
        # just to distinguish it in the graph
        # bc var x is not the same as f(x) (they are mapped)
        f: Callable # not fmap
        p: str

    def __init__(self, con: Connect, **attrs):
        self.con = con
        from networkx import DiGraph
        self.graph = DiGraph(**attrs)

    def add_F(self, fm: FMap):
        _ = fm.graph()
        self.graph.update(_)
