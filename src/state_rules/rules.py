# this seems like a 'low' level primitive
# (to build on)
from typing import Any, Self

class types:
    state_key = int | str # hashable?
    state = dict # can it be something else? just need mapping and iter
    type var = str
    type argpos = int
    from typing import Any, Literal
    returnkey = Literal['return']
    multioutkeys = tuple | list | set | frozenset
    argmap = dict[var | argpos | returnkey , state_key | multioutkeys ]

from typing import Callable


class Data:
    def dataclass(c):
        from dataclasses import dataclass
        return dataclass(frozen=True)(c)
    @dataclass
    class Block:
        i: int
        f: Callable
        iz: frozenset[types.var]
        oz: frozenset[types.state_key]
    @dataclass
    class VarMap:
        i: int
        f: Callable
        arg:        types.var
        state_key:  types.state_key
    @dataclass
    class State:
        k: types.state_key
        from typing import Any
        v: Any

    @dataclass
    class F: # just represents a copy to be 1:1 with Block
        # use wrapt?
        from typing import Callable
        f: Callable
        i: int
        #def __repr__(self) -> str: # cant use in dict key if this is here! why?!
        from functools import cached_property
        @cached_property
        def name(self):
            f = self.f
            _ = repr(f)
            _ = _.strip('"').strip("'")
            if _.startswith('<') and _.endswith('>'):
                mod = (f"{f.__module__}.") if (f.__module__ != '__main__') else ''
                return f"{mod}{f.__name__}"
            else:
                return _
        
        from functools import cached_property
        @cached_property
        def parameters(self):
            from inspect import signature
            return signature(self.f).parameters
        # cannot set another name for cached_property
        # params = parameters
        @cached_property 
        def params(self): return self.parameters

        @property
        def signature(self):
            from inspect import signature
            return signature(self.f)
        sig = signature
        
            
        def __call__(self, *p, **k):
            return self.f(*p, **k)

        
        @property
        def __name__(self): return self.f.__name__
        @property
        def __module__(self):   return self.f.__module__

    @dataclass
    class Arg:
        fidx: int
        name: types.var


    @dataclass
    class Graph:
        class types:
            node_key = types.state_key | types.var
            attribs = dict[str, types.Any]
        _ = types()
        nodes: dict[_.node_key , _.attribs]
        edges: dict[_node_key, _.node_key]
        del _
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
                class state:
                    state = 'state'
                    value = 'value'
            
            value = 'value'
            label = 'label'

class Rules:

    def __init__(self, state: types.state = {}, *, log: bool=False):
        self.state = state
        self.funcs = []
        self.log = [] if log is True else False


    def add_func(self, f, argmap: types.argmap = {}):
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
                return_statekey = argmap['return'],)
        self.funcs.append(_)
        return _
    register_func = add_func
    class FMap:
        def __init__(self, *, f, argmap, return_statekey):
            self.f, self.argmap, self.return_statekey = f, argmap, return_statekey
        def __repr__(self):
            from types import SimpleNamespace as NS
            _ = NS(f=self.f, argmap=self.argmap, return_statekey=self.return_statekey)
            _ = repr(_)
            _ = _.replace('namespace', self.__class__.__name__)
            return _


    def data(self: Self):
        rules = self
        for i, f in enumerate(rules.funcs):
            fn = f.f
            if not isinstance(f.return_statekey, types.multioutkeys):
                oz = (f.return_statekey,)
            else:
                assert(isinstance(f.return_statekey, types.multioutkeys))
                oz = f.return_statekey
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
                if not isinstance(fb.return_statekey, types.multioutkeys):
                    if fb.return_statekey not in self.state:
                        yield fb.return_statekey,\
                                {trm.types.type: trm.types.state.state,
                                trm.label: str(fb.return_statekey),}
                else:
                    for rsk in fb.return_statekey:
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
                if not isinstance(fb.return_statekey, types.multioutkeys):
                    src = Node(fb.f,                trm.types.f.    function)
                    dst = fb.return_statekey
                    add(src, dst, {trm.types.type: trm.types.f.binding.output })
                else:
                    for rsk in fb.return_statekey:
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
        common = frozenset(self.state) & frozenset(other.state)
        for c in common:
            if self.state[c] != other.state[c]:
                raise ValueError(f'state clash for key {c}: {self.state[c]}={other.state[c]}')
        from copy import deepcopy as copy
        new = copy(self)
        new.log = []  # clear this though 
        new.funcs.extend(other.funcs)
        new.state.update(other.state)
        return new

   
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

    
    def _apply(self, state: types.state):
        s = state
        for fm in self.funcs:
            try:
                _ = {a:s[sk] for a,sk in fm.argmap.items()  }
            except KeyError:
                continue
            _ = fm.f.f(**_) # take the inner one for performance
            if isinstance(fm.return_statekey, types.multioutkeys):
                # special case
                # the intent is to not output
                # could skip func app but could be a useful thing
                if not fm.return_statekey: 
                    continue
                elif isinstance(_, dict):
                    for sk in fm.return_statekey:
                        assert(sk in _)
                    s.update(_)
                else: # make one
                    _ = dict.fromkeys(fm.return_statekey, _)
                    s.update(_)
            else:
                s[fm.return_statekey] = _
            yield fm, s

    def _pre_flight(self):
        returns = set()
        for fm in self.funcs:
            if isinstance(fm.return_statekey, types.multioutkeys):
                returns.update(fm.return_statekey)
            else:
                returns.add(fm.return_statekey)
        for fm in self.funcs:
            for a,sk in fm.argmap.items():
                if          (sk in self.state) or (sk in returns): ...
                else: raise KeyError(f'{fm.f.name}{a} will not be bound.')

    def run(self, maxiter = 10, *,
                stopping: Callable[[types.state], bool] | None = None,
                preflight: bool = True,
                print_log:bool = False, # TODO: print i
                ):
        if preflight: self._pre_flight()
        i = self.i = 0
        from types import SimpleNamespace as NS
        class Iteration(NS):    pass

        from copy import deepcopy as copy
        # shallow vs deep copy? deep more general. shallow for simple objects.
        # maybe no performance loss if state is shallow.
        if self.log is not False:
            self.log.append(Iteration(i=i, state=copy(self.state)))
        if stopping is not None:
            if stopping(self.state): return self.state

        while True:
            if i >= maxiter:
                from warnings import warn
                warn('Reached iteration limit!')
                break
            # alt. is to 'old*hash*' == new*hash* to potentially avoid copying
            oldstate = copy(self.state)
            s = self.state
            for f,s in self._apply(self.state):
                if self.log is not False:
                    self.log.append(
                        Iteration(i=i+1,
                            state=copy(s),
                            rule=f,) )
                if stopping is not None:
                    if stopping(s): return s
            self.state = newstate = s

            if newstate == oldstate: # b/c of this, have to copy
                break
            else:
                i = i+1
                newstate = oldstate
                continue
            
        return self.state

    def __call__(self, *,
            _maxiter=999, _stopping=None,
            _print_log=False,
            **state) -> types.state:
        """treat the machine as a function:
        Keyword arguments will update the state.
        If a dictionary with the key 'state' is passed,
        its value will update the state.
        (So to have a 'state' key with a dictionary, you can nest it: (state={'x': 3, 'state': 5})
        """
        # should cache functions?
        if 'state' in state:
            assert(isinstance(state['state'], types.state))
            self.state.update(state.pop('state'))
        else:    
            self.state.update(**state)
        _ = self.run(maxiter=_maxiter, stopping=_stopping, print_log=_print_log)
        return self.state
