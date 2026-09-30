import inspect
from functools import cached_property
try: from icecream import ic
except ImportError: pass
"""
this module only deals with connectivity.
there are minimal contraints
"""
# this seems like a 'low'-level primitive
# (to build on)
# it does not deal with
# compositition (execpt a + op for mapped functions)
# or execution.


# this seems like a 'low' level primitive
# (to build on)
# it just deals with connectivity
from typing import Any, Self, Callable, Iterable, Hashable, Literal
def dataclass(c):
    from dataclasses import dataclass
    return dataclass(frozen=True)(c)

class reprs:
    @staticmethod
    def unquote(s: str):
        if not s: return s
        _ = s
        _ = _.strip('"')
        _ = _.strip("'")
        return _
    uq = unquote

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


    class Set(frozenset):
        def __repr__(self):
            _ = (io for io in self)
            _ = map(repr, _)
            _ = map(reprs.unquote , _)
            _ = sorted(_, key=str) # ok. for determinism
            _ = ','.join(_)
            _ = '{'+_+'}' # lol
            return _
    class IO(Set): pass

    class IOMap(iomap):
        """inside-->outside"""
        # should not change.
        # lives in FMap(frozen)
        def __hash__(self):
            return hash(tuple(sorted(self.items())))
        
        def __repr__(self):
            def io(i,o):
                _ = map(str, (i,o))
                _ = map(reprs.unquote, _)
                i,o = _
                _ = f"{i}→{o}"
                return _
            rk = types.returnkeyvalue
            iz = {k:v for k,v in self.items() if k!=rk}
            iz = '\n'.join(io(k,    v) for (k,v) in  iz.items())
            if rk in self:
                if not isinstance(self[rk], dict):
                    oz =  set(self[rk])
                    oz = '\n'.join(io('', o) for o in oz )
                else:
                    oz = self[rk].items()
                    oz = '\n'.join(io('','')+io(ri,ro) for ri,ro in oz)
            else:
                oz = ''
            return '\n'.join((iz,oz))


from .vis.utils import strops

class exceptions:
    class ValueNotFound(KeyError): pass



@dataclass
class FMap:
    # use wrapt?
    """
    reresents mapping from vars/state to f
    """
    iomap: types.iomap
    from typing import Callable
    i: types.IO
    f: Callable
    o: types.IO
    # idx: int # should order matter? does it make sense to register a function with the same inputs and outputs?

    from functools import cached_property

    @classmethod
    def from_iomap(cls, f, iomap: types.iomap):
        returnkey  = types.returnkeyvalue
        if returnkey not in iomap:
            raise AssertionError(f"{returnkey} not in fmap.")
        from inspect import signature 
        sig = signature(f)
        argmap = {k:v for k,v in iomap.items() if k != returnkey}
        argmap = cls.kwargmap(f, types.IOMap(argmap) )
        # just try to, to raise exception if issue
        sig.bind(**{a:None for a in argmap })
        if isinstance(iomap[returnkey], (set, list, frozenset, tuple, )):
            returns = iomap[returnkey]
            rm = frozenset(returns)
        elif isinstance(iomap[returnkey], dict):
            returns = iomap[returnkey].values()
            rm = types.IOMap(iomap[returnkey])
        else:
            returns = {iomap[returnkey], }
            rm = frozenset(returns)
        return cls(
            iomap = types.IOMap({**argmap, **{returnkey: rm }}),
            i=types.IO(argmap.values()),
            f=f,
            o=types.IO(returns),
            )


    from functools import cache
    @staticmethod         
    @cache                  
    def kwargmap(f, argmap: types.IOMap, inv=False) -> dict[types.kw, types.var_key] | dict[types.var_key, types.kw] :
        """
        replace positionally placed args with keywords as a 'normalization'
        """
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

    def __repr__mapped(self) -> str:
        i, o = map(lambda _: '{}' if not _ else '{'+repr(_)+'}' , (self.i, self.o))
        _ = f"{self.fname}:{i}→{o}"
        return _
    def __repr__(self) ->str:
        oz = types.IO(frozenset(self.o))
        def am():
            for farg, v in self.argmap.items():
                _ = f'{v}→{farg}'
                yield _
        am = ','.join(am())
        _ = f"{self.fname}({am})→{oz}"
        return _

    @cached_property
    def fname(self):
        f = self.f
        _ = str(f)
        _ = _.strip('"').strip("'")
        if _.startswith('<') and _.endswith('>'):
            mod = (f"{f.__module__}.") if (f.__module__ != '__main__') else ''
            _ = f"{mod}{f.__name__}"
            return _
        else:
            return _
    
    @property
    def conn(self) ->Connecting:
        _  = Connecting()
        _.add_fmap(self)
        return _
    
    # application
    
    @cached_property
    def argmap(self) -> types.argmap:
        _ = {k:v for k,v in self.iomap.items() if k != types.returnkeyvalue}
        return _

    def finput(self, values: dict[types.var_key, Any], argmap: types.argmap|None=None):
        _ = self.argmap if argmap is None else self.kwargmap(self.f, types.IOMap(argmap) )
        try:
            _ = {kw:values[k] for kw, k in _.items()}
        except KeyError:
            for kw, k in _.items():
                if k not in values:
                    raise exceptions.ValueNotFound(
            f"Value key {k} for {self.fname}({kw}) not found in given values.")
        return _

    @cached_property
    def fbind(self):
        from inspect import signature
        return signature(self.f).bind

    def __call__(self, values: dict[types.var_key, Any], argmap: types.argmap|None=None):
        _ = self.finput(values, argmap)
        _ = self.fbind(**_)
        _ = self.f(*_.args, **_.kwargs) # here _.kwargs are kw-only
        _ = self.returns(_)
        return _

    @cached_property
    def returnsmap(self):
        return (True if isinstance(self.iomap[types.returnkeyvalue], types.IOMap)
        else    False)
    @cached_property
    def returns1(self):
        return (True if len(self.o) == 1
        else    False)
    def returns(self, r: dict | Any) -> dict: # an update
        if self.returnsmap:
            rm = self.iomap[types.returnkeyvalue]
            assert(isinstance(r, dict))
            return {ro:r[ri] for ri,ro in rm.items()}
        # 'regular' f o
        if self.returns1:
            (o, ) = self.o
            return {o: r}
        else: # just copying
            return {o:r for o in self.o}
        raise Exception('return not handled.')

    from networkx import DiGraph
    def graph(self) -> DiGraph:
        from networkx import DiGraph
        g = DiGraph()
        terms = Graph.terms
        label = Graph.terms.label
        type = terms.types.type
        def uqr(o):
            _ = repr(o)
            _ = strops.uq(_)
            return _
        # INPUT outside in
        for farg,var in self.argmap.items():
            # outside->in
            farg = Graph.FArg(self, farg)
            g.add_node(var,  
                **{type: terms.types.variable.  variable,   label:uqr(var) })
            g.add_node(farg,
                **{type: terms.types.f.         arg,        label:uqr(farg) })
            g.add_edge(var, farg,
                **{type: terms.types.f.         binding.binding     })
            g.add_edge(farg, self,
                **{type: terms.types.f.binding. input     })

            del farg, var
        # F 'in'
        g.add_node(self,
                **{type :terms.types.f.         function,   label:uqr(self.fname)})
        # OUTPUT in -> outside
        for o in self.o:
            g.add_edge(self, o,
                **{type: terms.types.f.binding. output })
            g.add_node(o,     
                **{type: terms.types.variable.  variable,   label:repr(o) })
            del o
        return g

    # for composition ops you'd have to create unique intermediate/non-interacting vars

from .vis.marimo import Display
class Connecting(Display):
    def __init__(self,
            fmaps: Iterable[FMap] =[],
            name = None,
            default_exec = ('state', {}),
            ):
        for fm in fmaps:
            self.add_func(fm)
        self.ops = []
        self._graph = Graph(name=name)
        self.graph = self._graph.graph
        self.name= name
        self._exec = default_exec
    
    def __repr__(self):
        _ = (self.name+':') if self.name else ''
        _ = (_+'\n' if _ else _) + '\n'.join(map(repr, self.fmaps))
        return _


    def add_func(self, f: Callable, iomap: types.iomap = {})-> FMap:
        # if isinstance(f, FMap): # meaningless recursion blocker
        #     assert(not iomap)
        #     return self.add_fmap(f)
        returnkey  = types.returnkeyvalue
        from inspect import signature
        sig = signature(f)
        if returnkey not in iomap:
            returns = FMap.from_iomap(f, {**{p:p for p in sig.parameters}, **{returnkey: ''}}).fname
            returns = returns + str(len(self.fmaps))
        else:
            returns = iomap[returnkey]
        for _ in iomap:
            if _ != returnkey:
                if _ not in sig.parameters:
                    raise KeyError(f'{_} not in function signature.')
            del _
        argmap = {
            n:n if n not in iomap 
                else iomap[n] for n,p in sig.parameters.items()
                    if ((p.default) == p.empty) }

        iomap = {**argmap, **{returnkey: returns}}
        fm = FMap.from_iomap(f, iomap)
        g = fm.graph()
        self.graph.update(g)
        return fm
    register_func = add_func

    def add_fmap(self, fm: FMap) -> FMap:
        c = self.__class__()
        _ = c.add_func(fm.f, fm.iomap)
        self.add_conn(c)
        return _

    @property
    def fmaps(self) -> tuple[FMap]:
        # i think same as insertion order
        def _():
            for n in self.graph.nodes:
                if self.graph.nodes[n][Graph.terms.types.type] == Graph.terms.types.f.function:
                    yield n
        return tuple(_())

    @property
    def fmap(self) -> FMap:
        def io(self):  
            """viewing all of con as a func"""
            fins = []
            _ = (fm.i for fm in self.fmaps)
            for oz in _: fins.extend(oz)
            fins = frozenset(fins)
            _ = (fm.o for fm in self.fmaps)
            fouts = []
            for iz in _: fouts.extend(iz)
            fouts = frozenset(fouts)
            return ( # neat!
                    fins  - fouts, # i
                    fouts - fins ) # o 
        i,o = io(self)
        class ConnFunc: # quite hacky
            def __init__(self, conn, i, o):
                self.conn = conn
                self.i = i
                self.o = o

            @property
            def __name__(self):
                return self.conn.name if self.conn.name else self.conn.__class__.__name__

            def __call__(self, **input: dict):
                _ = self.conn(**input)
                return _
            
            @property
            def fakeargmap(self):
                return  {f'_{i}':p for i,p in enumerate(self.i)}
            @property
            def fakesig(self):
                from inspect import Signature, Parameter, _ParameterKind
                ps = []
                for fa,ra in self.fakeargmap.items():
                    p = Parameter(fa, _ParameterKind.KEYWORD_ONLY)
                    p._name = ra
                    ps.append(p)
                _ = Signature(ps)
                return _
            __signature__ = fakesig
            
        f = ConnFunc(self, i,o)
        fm = FMap.from_iomap(f, {**{i:i for i in f.i}, **{'return': {o:o for o in f.o} }} )
        return fm

    def register(self, iomap: types.iomap = {}, ):
        """decorator """ 
        if callable(iomap): # case when no (parens) used @register
            f = iomap
            argmap = {} # the default
            self.add_func(f)
            return f
        else:
            def decorator(f, iomap=iomap):
                self.add_func(f, iomap=iomap)
                return f
            return decorator

    def add_conn(self, other: Self) -> None:
        for fm in other.fmaps:
            self.add_func(fm.f, fm.iomap)
        return None

    @property
    def sets(self):
        from .struct.set import Sets
        _ = Sets(self)
        return _
    

    #def __add__(self, other: Self):
    #    symmetric expectation: which properties like name shoud take?
    #    return self.add(other)
    def add(self, other: Self| Callable, **k)-> None:
        if isinstance(other, type(self)):
            _ = self.add_conn(other, **k)
        else:
            assert(isinstance(other, Callable))
            _ = self.add_func(other, **k)
        return None

    def __eq__(self, other: Self) -> bool:
        return self._graph == other._graph


    @cached_property
    def exec(self):
        _ = getattr(self.execs, self._exec[0])
        del self._exec
        return _

    def __call__(self, *p, **k):
        _ = self.exec
        _ = _(*p, **k)
        return _

    @cached_property
    def execs(self):
        from .exec import Execs
        _ = Execs(self, inits={self._exec[0]: self._exec[1]})
        return _


class Graph:
    class terms:
        class types:
            type =  'type'
            class f:
                function = 'function'
                arg =   'arg'
                class binding:
                    binding = 'binding'
                    input = 'input'
                    output = 'output'
            class variable:
                variable =  'variable'
        value = 'value'
        label = 'label' 

    @dataclass
    class FArg:
        # just to distinguish it in the graph
        # bc var x is not the same as f(x) (they are mapped)
        fm: FMap
        p: str
        def __repr__(self):
            _ = f"{self.fm.fname}({self.p})"
            return _
    

    def __init__(self, **attrs):
        from networkx import DiGraph
        self.graph = DiGraph(**attrs)


    def __eq__(self, other: Self) -> bool:
        #from networkx.utils import graphs_equal
        #_ = graphs_equal(self.graph, other.graph)
        # not giving the same as
        from networkx.utils import nodes_equal, edges_equal
        ne = nodes_equal(self.graph.nodes, other.graph.nodes)
        ee = edges_equal(self.graph.edges, other.graph.edges, directed=True)
        return ne and ee
        st = frozenset
        ne = st(self.graph.nodes) == st(other.graph.nodes)
        ee = st(self.graph.edges) == st(other.graph.edges)
        return ne and ee
