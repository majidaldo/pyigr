from ast import Call
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
        self.add(init)

    def __repr__(self) -> str:
        return repr(self.list)

    @property
    def prv(self):
        if len(self.list)>=2:
            return self.list[-2]
        else:
            return None
    @property
    def cur(self): return self.list[-1]

    def add(self, s: dict | types.State):
        if not isinstance(s, types.State): s = types.State(s)
        from copy import deepcopy as copy
        # shallow vs deep copy? deep more general. shallow for simple objects.
        # maybe no performance loss if state is shallow.
        s = copy(s)
        return self.list.append(s)
    append = add

    @property
    def changed(self) -> bool | None:
        # b/c of this, have to copy in self.add
        if len(self.list)>=2:
            return self.prv != self.cur
        else:
            return None


@dataclass
class Application:
    input: dict
    fmap: FMap
    returns: dict
    @classmethod
    def get_input(cls, fm: FMap, state: dict):
        return fm.finput(state)


class Run:
    def __init__(self,
        conn: Connecting, *,
            check: set|list|tuple|frozenset = ('binding',), # 'flow'), # TODO
            cache: bool | Callable =True , 
            ):
        #for chk in check: getattr(conn, '_chk_'+chk)()
        self.conn = conn
        self.states = States()
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

    def _oneupdate(self, state: types.State ):
        for fm in self.conn.fmaps:
            _ = state
            _ = self.maybecached(fm, values=_)
            rs = fm.returns(_)
            state.update(rs)
            yield state, fm, rs

    def run(self,
            state: dict, maxiter=999, *,
                stopping: Callable[[types.State], bool ]=None,
                log = False,
                ):
        i = 0 # 
        states = States(state,)
        log = [] if log else False

        maxediter = False
        while True:
            if i >= maxiter:
                from warnings import warn
                warn('Reached iteration limit!')
                maxediter = True
                break
            if stopping is not None:
                if stopping(states.cur):
                    break
            for s, fm, rs in self._oneupdate(states.cur):
                if log is not False:
                    input = Application.get_input(fm, s)
                    log.append(
                        Application(input, fm, rs)
                    )
            states.add(states.cur)
            if states.changed:
                continue
            else:
                break
        
        from types import SimpleNamespace as NS
        return NS(
            state = states.cur,
            log = log,
            maxediter = maxediter)

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
