try: from icecream import ic
except ImportError: pass
# seems like bootstrapping the system.
from warnings import warn
from ..connecting import FMap, Connecting, Callable, Any

class types:
    from ..connecting import types as contypes
    value = Any
    state = dict[contypes.var_key, value]

    class State(state):
        def __hash__(self):
            return hash(tuple(sorted(self.items())))
        def __repr__(self) -> str:
            if len(self)>10:
                return f'{self.__class__.__name__} too big to display meaningfully.'
            else:
                return super().__repr__()
    class Values(State): pass

def dataclass(c):
    from dataclasses import dataclass
    return dataclass(frozen=True)(c)
from dataclasses import field

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

    from ..connecting import exceptions as cx
    def _oneupdate(self, state: types.State ):
        for fm in self.conn.fmaps:
            _ = state
            try:
                _ = self.maybecached(fm, values=_)
            except self.cx.ValueNotFound as vnf:
                warn(vnf.args[0])
                continue
            rs = fm.returns(_)
            state.update(rs)
            yield state, fm, rs

    class Log(list):
        def __repr__(self) -> str:
            return '.log'

    def run(self,
            state: dict, maxiter=999, *,
                stopping: Callable[[types.State], bool ]|None=None,
                log = False,):
        i = 0 # 
        states = States(state,)
        log = self.Log([]) if log else False
        maxediter = False
        from copy import deepcopy as copy
        # shallow vs deep copy? deep more general. shallow for simple objects.
        # maybe no performance loss if state is shallow.
        while True:
            if i >= maxiter:
                if i>0: warn('Reached iteration limit!')
                maxediter = True
                break
            if stopping is not None:
                if stopping(states.cur):
                    break
            
            cur = copy(states.cur)
            for s, fm, rs in self._oneupdate(cur):
                if log is not False:
                    input = Application.get_input(fm, s)
                    log.append(
                        Application(input, fm, rs))
                    from copy import deepcopy as copy
            states.add(cur) # now we have an 'old'
            if not states.changed:
                break
            else:
                i+=1
                continue
        
        return self.Return(
            state = states.cur,
            log = log,
            maxediter = maxediter)
    @dataclass
    class Return:
        state: types.State
        log: bool | list[Application] 
        maxediter: bool

    def __call__(self, state: types.state, **run_kwargs):
        """
        treat the machine as a function: state is input and output
        """
        _ = self.run(state, **run_kwargs)
        return _.state

