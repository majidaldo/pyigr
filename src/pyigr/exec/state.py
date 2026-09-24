try: from icecream import ic
except ImportError: pass
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
# reactiv is interesting but want circular deps

def dataclass(c):
    from dataclasses import dataclass
    return dataclass(frozen=True)(c)

class Values(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

# want
from reaktiv import signal, computed, ComputeSignal as _ComputeSignal
# internal
from reaktiv import graph
from typing import cast, TypeVar
T = TypeVar("T")

class ComputeSignal(_ComputeSignal):
    def get(self):
        # Thread-safe circular dependency detection
        if self._is_running_in_current_thread():
            return True
            raise RuntimeError("Circular dependency detected")

        self._refresh()

        # participate as producer if someone depends on us
        edge = graph.add_dependency(self)
        if edge is not None:
            edge.version = self._version
        if self._flags & graph.HAS_ERROR:
            assert self._last_error is not None
            raise self._last_error
        return cast(T, self._value)


# can this be reworked with python setters and getters?
    # def __repr__(self):
    #     # the arrow thing is for when this can be viewed as a 'function'
    #     name = self.name if self.name else self.__class__.__name__
    #     if self.name:
    #         _ = map(set, self.io)
    #         i,o = map(lambda _: '{}' if not _ else repr(_), _)
    #         _ = f"{name}({i}→{o})"
    #         return _
    #     else:
    #         return repr(super().__init__())
# just print out vars



# typing from graph

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

    # def _chk_binding(self):
    #     returns = set()
    #     for fm in self.funcs:
    #         returns.update(fm.return_statekeys)
    #     for fm in self.funcs:
    #         for a,sk in fm.argmap.items():
    #             if          (sk in self.state) or (sk in returns): ...
    #             else: raise KeyError(f'{fm.f.name}{a} will not be bound.')
    # def _chk_flow(self):
    #     # no circles
    #     # chk distinct inputs outputs
    #     ...

    
    # @property
    # def io(self):  # io?
    #     # self._chk_binding() need to?
    #     _ = (fb.argmap.values() for fb in self.funcs)
    #     fins = []
    #     for os in _: fins.extend(os)
    #     fins = frozenset(fins)
    #     _ = (fb.return_statekeys for fb in self.funcs)
    #     fouts = []
    #     for iz in _: fouts.extend(iz)
    #     fouts = frozenset(fouts)
    #     return Data.IO(
    #             input=fins   - fouts,
    #             output     = fouts - fins) # neat


    # def run(self,
    #         maxiter = 10, *,
    #             stopping: Callable[[types.state], bool] | None = None,
    #             check: set|list|tuple|frozenset = ('binding',), # 'flow'),
    #             print_log:bool = False, # TODO: print i
    #             cache=True, # starting to think this a good default TODO
    #             ):
    #     for chk in check: getattr(self, '_chk_'+chk)()
    #     i = self.i = 0
    #     from types import SimpleNamespace as NS
    #     class Iteration(NS):    pass

    #     from copy import deepcopy as copy
    #     # shallow vs deep copy? deep more general. shallow for simple objects.
    #     # maybe no performance loss if state is shallow.
    #     if self.log is not False:
    #         self.log.append(Iteration(i=i, state=copy(self.state)))
    #     if stopping is not None:
    #         if stopping(self.state): return self.state

    #     # this could just use python's setters and getters.
    #     # but i think there's more control with the below
    #     while True:
    #         if i >= maxiter:
    #             from warnings import warn
    #             warn('Reached iteration limit!')
    #             break
    #         # alt. is to 'old*hash*' == new*hash* to potentially avoid copying
    #         oldstate = copy(self.state)
    #         s = self.state
    #         for f,s in self._apply(self.state):
    #             if self.log is not False:
    #                 self.log.append(
    #                     Iteration(i=i+1,
    #                         state=copy(s),
    #                         rule=f,) )
    #             if stopping is not None:
    #                 if stopping(s): return s
    #         self.state = newstate = s

    #         if newstate == oldstate: # b/c of this, have to copy
    #             break
    #         else:
    #             i = i+1
    #             newstate = oldstate
    #             continue
            
    #     return self.state

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