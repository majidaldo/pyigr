# this seems like a 'low' level primitive
# (to build on)
# it just deals with connectivity
from typing import Any, Self, Callable, Iterable, Hashable, Literal

class types:
    var_key = Hashable
    type kw = str
    type arg = kw | int
    returnkey = Literal['return']
    multioutkeys = tuple | frozenset
    argmap = dict[arg, var_key] 
    fmap: dict[arg | returnkey, var_key | multioutkeys]

    class IO(frozenset):
        def __repr__(self):
            _ = (io for io in self)
            _ = map(repr, _)
            _ = map(lambda l: sorted(l, key=str),  _)
            _ = map(lambda _: _.replace('"', '').replace("'", '' ) , _)
            _ = ','.join(_)
            return _

def dataclass(c):
    from dataclasses import dataclass
    return dataclass(frozen=True)(c)
@dataclass
class F:
    # use wrapt?
    """
    reresents mapping from vars/state to f
    """
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
    def from_fmap(cls, f, fmap: types.fmap):
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
        if isinstance(fmap[returnkey], types.multioutkeys):
            returns = fmap[returnkey]
        else:
            returns = {fmap[returnkey], }
        return cls(
            i=frozenset(argmap.values()),
            f=f,
            o=frozenset(returns))


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
        if inv: {v:k for k,v in argmap.items()}
        return argmap


    def __post_init__(self):
        # sorting to make order not matter (does that make sense?!)
        object.__setattr__(self, 'i', frozenset(sorted(self.i, key=str)))
        object.__setattr__(self, 'o', frozenset(sorted(self.o, key=str)))

    def __repr__(self) -> str:
        i, o = map(lambda _: '{}' if not _ else '{'+repr(_)+'}' , _)
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
    @cached_property
    def bind(self): return self.sig.bind

    @cached_property
    def __name__(self): return self.f.__name__
    @cached_property
    def __module__(self):   return self.f.__module__

    
    # application
    # should be able to put these functions on some execution

    def __call__(self, values: dict[types.var_key, Any] | tuple[Any], argmap: types.argmap | None =None ):
        if isinstance(values, dict):
            _ = argmap
            _ = tuple(argmap.items())  #TODO hashable
            _ = self.kwargmap(self.f, _)
            # user can check if argmap values are in values
            _ = {kw:values[k] for kw, k in _.items()}
            _ = self.bind(**_)
        else:
            assert(argmap is None)
            _ = values
            _ = self.bind(*_)
        return self.f(*_.args, **_.kwargs) # here _.kwargs are kw-only

    def returns(self, r: dict | Any): # an update
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



class Connect:
    def __init__(self, fmaps=[]):
        for f, argmap in fmaps:
            self.add_func(f, argmap)
        self.ops = []

    def _add_op(self,  selfop, kwargs, nodes, edges):
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
            (selfop, kwargs, nodes, edges)
        )

    def add_func(self, f, fmap: dict = {}):
        from typing import get_args
        returnkey  : types.returnkey = get_args(types.returnkey)[0]
        from inspect import signature
        sig = signature(f)
        argmap = {k:v for k,v in fmap.items() if k!=returnkey }
        if not fmap:
            argmap = {p:p for p in  sig.parameters}
        
        F.kwargs(f, )

        if returnkey not in argmap:
            argmap['return'] = f"{f.name}[{f.i}]" # f'{f.__module__}.{f.__name__}()'

        self.funcs.append(_)
        #self._add_op(self.add_func, f=f, nodes, edges)
        return _
    register_func = add_func

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
