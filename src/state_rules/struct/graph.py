from ..rules import Rules as _Rules, types


class Rules(_Rules):
    def mermaid(self, log_idx=-1):
        return mermaid(self, log_idx=log_idx)
    
    def _display_(self):
        _ = mermaid(self)
        from marimo import mermaid as md
        _ = md(_)
        return _


from typing import Callable
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
def data(rules: Rules):
    for i, f in enumerate(rules.funcs):
        fn = F(f.f)
        if not isinstance(f.return_statekey, types.multioutkeys):
            oz = (f.return_statekey,)
        else:
            assert(isinstance(f.return_statekey, types.multioutkeys))
            oz = f.return_statekey
        yield Block(i=i,
            f = fn,
            iz = frozenset(f.argmap.keys()),
            oz = frozenset(oz))
        for arg, statekey in f.argmap.items():
            yield VarMap(i = i,
                f = fn,
                arg = arg,
                state_key = statekey
            )
    for k,v in rules.state.items():
        yield State(k=k,v=v)

class F: # just represents a copy to be 1:1 with Block
    def __init__(self, f):
        self.f = f
    def __repr__(self) -> str:
        return frepr(self.f)
    def __call__(self, *p, **k):
        return self.f(*p, **k)
    @property
    def __name__(self):     return self.f.__name__
    @property
    def __module__(self):   return self.f.__module__


def nxgraph(rules: Rules):
    from networkx import DiGraph
    g = DiGraph()
    for d in data(rules):
        if isinstance(d, Block):
            g.add_node(d.f,     type='f',   label=repr(d.f))
            for i in d.iz:
                g.add_node(i,   type='i',   label=repr(i))
                g.add_edge(i, d.f,)
                del i
            for o in d.oz:
                g.add_node(o,   type='o',   label=repr(o))
                g.add_edge(d.f, o, )
                del o
        else:
            assert(isinstance(d, VarMap))
            if d.arg != d.state_key:
                g.add_edge(d.state_key, d.arg)
        del d
    return g


def frepr(f):
    _ = repr(f)
    _ = _.strip('"').strip("'")
    if _.startswith('<') and _.endswith('>'):
        mod = (f"{f.__module__}.") if (f.__module__ != '__main__') else ''
        return f"{mod}{f.__name__}"
    else:
        return _


def value_repr(v):
    _ = str(v)
    _ = _.strip('"').strip('"')
    if len(_)>20:
        _ = _[:20]
        _ = _+'...'
    return _


def mermaid(rules: Rules, log_idx=-1):
    if log_idx == -1:
        state = rules.state
    else:
        state = rules.log[log_idx].state
    # really wanted svelte flow
    #---
    # title: repr(rules)
    # ---
    # flowchart TD
    #     input
    #     A((A)) -->|i1|f
    #     A((A)) -->|i2|f
    #     output
    #     f -->o1((o1))
    #     f -->o2((o2))
    def part(n, type, id=id, ):
        v = val
        if type == 'f':
            return f"{type}{id(n)}[\\{ frepr(n) }/]"
        if type in {'s', 'o'}:
            return f"so{id(n)}@{{shape: stadium, label: {frepr(n)+val(n, type, )} }}"
        if type == 'i':
            return f"|{repr(n).strip('"').strip("'")}|"
        raise Exception('not handled')

    def val(n, type, ):
        if type =='f':
            return ''
        elif n not in state:
            return ''
        v = state[n]
        v = value_repr(v)
        v = '='+v
        return v

    def parts(r: Block | VarMap | Rules):
        if isinstance(r, Block):
            block = r
            for o in block.oz:
                yield f"{part((block.f), 'f')}-->{part(o, 'o')}"
            if not block.iz:
                yield part((block.f), 'f')
        elif isinstance(r, VarMap):
            vm = r
            yield f"{part(vm.state_key, 's')}-->{part(vm.arg, 'i')}{part(vm.f, 'f')}"
        elif isinstance(r, State):
            if not rules.funcs:
                yield f"{part(r.k, 's')}"
        else:
            assert(isinstance(r, Rules))
            for d in data(r):
                yield from parts(d)
    
    _ = parts(rules)
    _ = '\n'.join(_)
    _ = f"""
    ---
    title: {repr(rules).strip('"').strip("'").strip('<').strip('>')}
    ---
    flowchart TD
    {_}
    """
    _ = (l.strip() for l in _.split('\n') if l.strip())
    _ = '\n'.join(_)
    return _
    

