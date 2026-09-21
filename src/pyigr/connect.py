# this seems like a 'low' level primitive
# (to build on)
# it just deals with connectivity
from typing import Any, Self, Callable, Iterable, Hashable, Literal

class types:
    var_key = Hashable
    type arg = str | int # kw, pos
    returnkey = Literal['return']
    multioutkeys = tuple | frozenset
    argmap = dict[arg | returnkey ,  multioutkeys ]



class Data:
    def dataclass(c):
        from dataclasses import dataclass
        return dataclass(frozen=True)(c)

    @dataclass
    class F: # just represents a copy to be 1:1 with Block
        # use wrapt?
        from typing import Callable
        i: frozenset
        f: Callable
        o: frozenset

        from functools import cached_property
        @cached_property
        def tuple(self): return (self.i, self.f, self.o)        

        def __post_init__(self):
            object.__setattr__(self, 'i', self.i)
            object.__setattr__(self, 'o', self.o)

        def __repr__(self) -> str:
            _ = map(set, (self.i, self.o) )
            i, o = map(lambda _: '{}' if not _ else repr(_), _)
            _ = f"{self.name}:{i}→{o}"
            return _

        @cached_property
        def name(self):
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
        
    
        def __call__(self, *p, **k):
            return self.f(*p, **k)

        @cached_property
        def __name__(self): return self.f.__name__
        @cached_property
        def __module__(self):   return self.f.__module__

    @dataclass
    class Arg:
        fidx: int
        name: types.var

    from collections import namedtuple as _
    IO = _('IO', ['input', 'output'])
    del _


##
# def uniqe_var. part of uuid is probably unique enough for a repr
##


class Connect:
    def __init__(self, argmaps=[]):
        for f, argmap in argmaps:
            self.add_func(f, argmap)

    def _add_op(self,  selfop, **kwargs):
        # chk args
        from copy import deepcopy as cp
        try:
            kwargs = cp(kwargs)
        except:  # idk
            from copy import copy
            kwargs = copy(kwargs)
        # check that all needed args are mapped
        from inspect import signature as sig
        sig(selfop).bind(**kwargs)
        self.ops.append(
            (selfop, kwargs)
        )

    def add_func(self, f, argmap: types.argmap = {}):
        self._add_op(self.add_func, f=f, argmap=argmap)
        f = Data.F(f, len(self.funcs)) #
        if not argmap:
            argmap = {p:p for p in f.parameters}
        # replace pos with kwargs
        for i, p in enumerate(f.parameters):
            if (i in argmap) and (p in argmap):
                raise KeyError(f'conflicting arguments: positional {i} and keyword {p} refer to the same argument.')
            else:
                if p not in argmap:
                    argmap[p] = p
                if i in argmap:
                    argmap.pop(i)
        for a in argmap:
            if isinstance(a, int):
                raise KeyError(f'positional argument {a} is not mapped.')
        # just try to, to raise exception if issue
        f.signature.bind(**{a:None for a in argmap if a!='return'})

        if 'return' not in argmap:
            argmap['return'] = f"{f.name}[{f.i}]" # f'{f.__module__}.{f.__name__}()'

        _ = self.FMap(
                f =  f,
                argmap = {fa:sk  for fa,sk in argmap.items() if (fa != 'return') },
                return_statekeys = {
                    argmap['return'],} if not isinstance(argmap['return'], types.multioutkeys)
                    else argmap['return'] ,)
        self.funcs.append(_)
        return _
    register_func = add_func
    class FMap:
        def __init__(self, *, f, argmap, return_statekeys):
            self.f, self.argmap, self.return_statekeys = f, argmap, return_statekeys
        def __repr__(self):
            from types import SimpleNamespace as NS
            _ = NS(f=self.f,
                    argmap=self.argmap,
                    return_statekeys=self.return_statekeys)
            _ = repr(_)
            _ = _.replace('namespace', self.__class__.__name__)
            return _
    def register(self, argmap: types.argmap = {}, ):
        """decorator """ 
        if callable(argmap): # case when no (parens) used @register
            f = argmap
            argmap = {} # the default
            self.add_func(f)
            return f
        else:
            def decorator(f, argmap=argmap):
                self.add_func(f, argmap=argmap)
                return f
            return decorator


    def data(self: Self):
        rules = self
        for i, f in enumerate(rules.funcs):
            fn = f.f
            oz = f.return_statekeys
            yield Data.Block(i=i,
                f = fn,
                iz = frozenset(f.argmap.keys()),
                oz = frozenset(oz))
            for arg, statekey in f.argmap.items():
                yield Data.VarMap(i = i,
                    f = fn,
                    arg = arg,
                    state_key = statekey
                )
        for k,v in rules.state.items():
            yield Data.State(k=k,v=v)

    def graph(self: Self)-> Data.Graph:
        """networkx-compatible data structure"""
        # intent to be 'data'/serialization
        trm = Data.Graph.terms
        Node = Data.Graph.Node
        Graph = Data.Graph
        Arg = Data.Arg
        def nodes(rules=self):
            self = rules
            for k,v in self.state.items():
                yield k,\
                        {trm.types.type: trm.types.state.state,
                         trm.label: str(k),
                        trm.types.state.value: v}
            for fi, fb in enumerate(self.funcs):
                yield Node(fb.f, trm.types.f.function),\
                    {trm.types.type:    trm.types.f.function,
                     trm.label: fb.f.name,
                     trm.types.f.i: fi,
                     trm.value: fb.f.f,
                     }
                # inputs
                for farg, statekey in fb.argmap.items():
                    if statekey not in self.state:
                        yield statekey,\
                                {trm.types.type: trm.types.state.state,
                                trm.label: str(statekey) }
                    yield Node( Arg(fi, farg), trm.types.f.arg),\
                            {trm.types.type: trm.types.f.arg,
                             trm.label: str(farg),
                             trm.value: farg,
                             }
                # outputs
                for rsk in fb.return_statekeys:
                    if rsk not in self.state:
                        yield rsk,\
                            {trm.types.type: trm.types.state.state}
        

        def edges(rules=self):
            ed = {} # edge dict
            def add(src, dst, attribs={}, ed=ed):
                if src not in ed:
                    ed[src] = {}
                #assert(dst not in ed[src])
                ed[src][dst] = attribs
                return ed

            for fi, fb in enumerate(rules.funcs):
                # state -> arg
                for farg, statekey in fb.argmap.items():
                    src = statekey
                    dst = Node(Arg(fi, farg),   trm.types.f.    arg)
                    add(src, dst,
                        {trm.types.type: trm.types.f.binding.input,
                        trm.types.f.function: fb.f.f },)
                # func -> state
                for rsk in fb.return_statekeys:
                    src = Node(fb.f,        trm.types.f.    function)
                    dst = rsk
                    add(src, dst,
                        {trm.types.type: trm.types.f.binding.output,
                        trm.types.f.function: fb.f.f})
            return ed
        
        return Graph(
            nodes={n:a for n,a in nodes()},
            edges=edges())
    #data = graph
    
    

    def __add__(self, other: Self): return self.add(other)
    def add(self, other):
        self._add_op(self.add, other=other)

        common = frozenset(self.state) & frozenset(other.state)
        for c in common:
            if self.state[c] != other.state[c]:
                raise ValueError(f'state clash for key {c}: {self.state[c]}!={other.state[c]}')
        from copy import deepcopy as copy
        new = copy(self)
        new.log = []  # clear this though 
        new.ops = []
        new.funcs.extend(other.funcs)
        new.state.update(other.state)
        return new




class Graph:
    """
    networkx compatible data
    """
    # but keep the state values separate
    class types:
        from dataclasses import dataclass
        @dataclass(frozen=True)
        class Node:    # need to uniquify
            from typing import Any
            obj: Any
            type: str # != 'state' for convenience


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
                value =     'value'     
        value = 'value'
        label = 'label'

    def __init__(self, rules: Rules):
        self.rules = rules
        self.graph = self.types.DiGraph()
        self.nodes = self.graph.nodes
        self.edges = self.graph.edges


    @property
    def state(self) -> dict:
        return {
            s:self.nodes[self.terms.types.state.value]
            for s in self.nodes
            if self.terms.types.state.value in self.nodes }


    def add_state(self, k, v: Any=None):
        attrs = {self.terms.types.state.value: v} if v is not None else {}
        self.graph.add_node(k, )
        return k, attrs
        

    def add_argmap(self, fm: Rules.FMap):
        ...


    def xgraph(self: Self)-> Data.Graph:
        """networkx-compatible data structure"""
        # intent to be 'data'/serialization
        trm = Data.Graph.terms
        Node = Data.Graph.Node
        Graph = Data.Graph
        Arg = Data.Arg
        def nodes(rules=self):
            self = rules
            for k,v in self.state.items():
                yield k,\
                        {trm.types.type: trm.types.state.state,
                         trm.label: str(k),
                        trm.types.state.value: v}
            for fi, fb in enumerate(self.funcs):
                yield Node(fb.f, trm.types.f.function),\
                    {trm.types.type:    trm.types.f.function,
                     trm.label: fb.f.name,
                     trm.types.f.i: fi,
                     trm.value: fb.f.f,
                     }
                # inputs
                for farg, statekey in fb.argmap.items():
                    if statekey not in self.state:
                        yield statekey,\
                                {trm.types.type: trm.types.state.state,
                                trm.label: str(statekey) }
                    yield Node( Arg(fi, farg), trm.types.f.arg),\
                            {trm.types.type: trm.types.f.arg,
                             trm.label: str(farg),
                             trm.value: farg,
                             }
                # outputs
                for rsk in fb.return_statekeys:
                    if rsk not in self.state:
                        yield rsk,\
                            {trm.types.type: trm.types.state.state}
        

        def edges(rules=self):
            ed = {} # edge dict
            def add(src, dst, attribs={}, ed=ed):
                if src not in ed:
                    ed[src] = {}
                #assert(dst not in ed[src])
                ed[src][dst] = attribs
                return ed

            for fi, fb in enumerate(rules.funcs):
                # state -> arg
                for farg, statekey in fb.argmap.items():
                    src = statekey
                    dst = Node(Arg(fi, farg),   trm.types.f.    arg)
                    add(src, dst,
                        {trm.types.type: trm.types.f.binding.input,
                        trm.types.f.function: fb.f.f },)
                # func -> state
                for rsk in fb.return_statekeys:
                    src = Node(fb.f,        trm.types.f.    function)
                    dst = rsk
                    add(src, dst,
                        {trm.types.type: trm.types.f.binding.output,
                        trm.types.f.function: fb.f.f})
            return ed
        
        return Graph(
            nodes={n:a for n,a in nodes()},
            edges=edges())

# class Running
# run

# class Tasks:
#  for topo sort.
