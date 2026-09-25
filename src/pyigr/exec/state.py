import types
try: from icecream import ic
except ImportError: pass
# seems like bootstrapping the system.
# can make a simple event loop
# each o deps on i. so can just keep track of new and old i.
# loop until no more changes
# can be in a set
# senitels
# class Unset: pass
# INIT, UNSET = Unset(), Unset()
# del Unset
# map fmap->(old inputs, new inputs).
#while true
# for fm in fmap:
    # if new!=old:
    #   do and set 
# max iters: break


from ..connecting import FMap, Connecting, Callable, Any

class types:
    from ..connecting import types as contypes
    value = Any
    state = dict[contypes.var_key, value]

    class State(state):
        def __hash__(self):
            return hash(tuple(sorted(self.items())))
    class Values(State): pass

def dataclass(c):
    from dataclasses import dataclass
    return dataclass(frozen=True)(c)


class States:
    def __init__(self, init: types.State | dict = types.State(),
                maxlen=2) -> None:
        init = types.State(init)
        from collections import deque
        self.list = deque(maxlen=maxlen)
        self.list.append(init)

    def __repr__(self) -> str:
        return repr(self.list)

    @property
    def old(self):
        if len(self.list)>=2:
            return self.list[-2]
        else:
            return None
    @property
    def cur(self): return self.list[-1]

    def add(self, s: dict | types.State):
        if not isinstance(s, types.State): s = types.State(s)
        return self.list.append(s)
    append = add

    @property
    def changed(self) -> bool | None:
        if len(self.list)>=2:
            return self.old != self.cur
        else:
            return None

class Run:
    def __init__(self,
        conn: Connecting,*,
            stopping: Callable[[types.state], bool] | None = None,
            check: set|list|tuple|frozenset = ('binding',), # 'flow'), # TODO
            log = False,
            print_log:bool = False, # TODO: print i
            cache: bool | Callable =True , 
            ):
        self.conn = conn
        self.i = 0
        self.stopping = stopping
        self.check = check
        self.print_log = print_log
        if cache:
            self.cachef = {}
            if cache is True:
                from functools import lru_cache
                cachef = lambda f: lru_cache(128)(f)
            else:
                cachef = cache
            for fm in conn.fmaps:
                self.cachef[fm] = cachef(fm)
        else:
            assert(cache is False)
            self.cachef = False # could be just unit but avoiding a func call
        


     
    from functools import cached_property
    @cached_property
    def fmaps(self): # assumes conn doesnt change
        return tuple(self.conn.fmaps)

    def maybecached(self, fmap, values):
        if self.cachef is False:
            return fmap(values)
        else:
            if not isinstance(values, types.Values):
                values = types.Values(values) # make hashable
            return self.cachef[fmap](values)

    #def _onefm(self, fm, s): maybe avoid the func call
    def _onepass(self, state:types.State, ):
        s = state
        for fm in self.conn.fmaps:
            _ = s
            _ = self.maybecached(fm, _)
            _ = fm.returns(_)
            yield fm, _

    # runiter?
    def run(self, maxiter=999):
        #for chk in check: getattr(self, '_chk_'+chk)()
        i = 0 # this i is 'internal' append to  self.i
        from copy import deepcopy as copy
        # shallow vs deep copy? deep more general. shallow for simple objects.
        # maybe no performance loss if state is shallow.
        if self.log is not False:
            self.log.append(Iteration(i=i, state=copy(self.state)))
        if stopping is not None:
            if stopping(self.state): return self.state

        # this could just use python's setters and getters.
        # but i think there's more control with the below
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

    # def __call__(self, *,
    #         _maxiter=999, _stopping=None,
    #         _check = {'binding', 'flow' },
    #         _print_log=False,
    #         **state) -> types.state:
    #     """treat the machine as a function:
    #     Keyword arguments will update the state.
    #     If a dictionary with the key 'state' is passed,
    #     its value will update the state.
    #     (So to have a 'state' key with a dictionary, you can nest it: (state={'x': 3, 'state': 5})
    #     """
    #     # should cache functions?
    #     if 'state' in state:
    #         assert(isinstance(state['state'], types.state))
    #         self.state.update(state.pop('state'))
    #     else:    
    #         self.state.update(**state)
    #     _ = self.run(
    #             maxiter=_maxiter, stopping=_stopping,
    #             check=_check,
    #             print_log=_print_log)
    #     return self.state

    # running
    
    # def _apply(self, state: types.state):
    #     s = state
    #     for fm in self.funcs:
    #         try:# can be binded?
    #             _ = {a:s[sk] for a,sk in fm.argmap.items()  }
    #         except KeyError:
    #             continue
    #         _ = fm.f.f(**_) # take the inner f for performance
    #         # special case
    #         # the intent is to not output
    #         # could skip func app but could be a useful thing
    #         if not fm.return_statekeys:
    #             continue
    #         elif isinstance(_, dict):
    #             for sk in fm.return_statekeys:
    #                 assert(sk in _)
    #             s.update(_)
    #         else: # make one
    #             _ = dict.fromkeys(fm.return_statekeys, _)
    #             s.update(_)
    #         yield fm, s
