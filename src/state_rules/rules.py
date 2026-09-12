# this seems like a 'low' level primitive
# (to build on)

class types:
    state_key = int | str # hashable?
    state = dict # can it be something else? just need mapping and iter
    type var = str
    from typing import Any, Literal
    returnkey = Literal['return']
    multioutkeys = tuple | list | set | frozenset
    argmap = dict[var | returnkey , state_key | multioutkeys ]
    

#class NO_RETURN(): ...
NO_RETURN = None #NO_RETURN() # senitel('no return') needs py 3.15

class Rules:

    def __init__(self, state: types.state = {}, *, log: bool=False):
        self.state = state
        self.funcs = []
        self.log = [] if log is True else False

    def add_func(self, f, argmap: types.argmap = {}):
        from inspect import signature
        if not argmap:
            argmap = {p:p for p in signature(f).parameters}
        for s in signature(f).parameters:
            if s not in argmap:
                argmap[s] = s
        if 'return' not in argmap:
            argmap['return'] = f # f'{f.__module__}.{f.__name__}()'

        _ = self.FMap(
            f = f,
            argmap = {fa:sk  for fa,sk in argmap.items() if (fa != 'return') },
            return_statekey = argmap['return'],)
        
        self.funcs.append(_)
    register_func = add_func
    class FMap:
        def __init__(self, *, f, argmap, return_statekey):
            self.f, self.argmap, self.return_statekey = f, argmap, return_statekey
    

    # __add__ would be nice since it's just appending self.funcs
   
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
        for f in self.funcs:
            _ = {a:s[sk] for a,sk in f.argmap.items() }
            _ = f.f(**_)
            # special case
            # could skip func app but could be a useful thing
            if f.return_statekey == NO_RETURN:
                continue
            if isinstance(f.return_statekey, types.multioutkeys):
                if isinstance(_, dict):
                    if len(f.return_statekey):
                        for sk in f.return_statekey:
                            assert(sk in _)
                else: # make one
                    _ = dict.fromkeys(f.return_statekey, _)
                s.update(_)
            else:
                s[f.return_statekey] = _
            yield f, s

    from typing import Callable
    def run(self, maxiter = 10, *, stopping: Callable[[types.state], bool] | None = None):
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
            if i >= maxiter: break
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

