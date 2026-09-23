from ..connecting import Connecting


class FlowChart:
    def __init__(self, conn: Connecting= Connecting()) -> None:
        self.conn = conn

    @property
    def title(self):
        
        _ = f"title: {repr(rules).strip('"').strip("'").strip('<').strip('>')}"
        return _


def flowchart(con: Connecting, log_idx=-1):
    assert(isinstance(conn: Connecting))
    if log_idx == -1 and (len(rules.log)==0):
        state = rules.state
    else:
        state = rules.log[log_idx].state

    def repr(o):
        for n in {'name', 'label', }:
            if hasattr(o, n):
                return getattr(o, n)
        return o.__repr__()
        

    from ..rules import Data
    terms = Data.Graph.terms
    from functools import cache
    @cache
    def part(n, type, id=id, label=None ):
        if label is None:
            label = repr(n).strip('"').strip("'")
        if type == terms.types.f.function:
            return f'{type}{id(n)}[\\"{ label }"/]'
        if type in {terms.types.state.state, }:
            return f'{type}{id(n)}@{{shape: stadium, label: "{label+val(n, type, )}" }}'
        if type == terms.types.f.arg :
            return f'{type}{id(n)}@{{shape: flip-tri, label: "{label }" }}'
        raise Exception('not handled')

    def val(n, type, ):
        if type == terms.types.f.function:
            return ''
        elif n not in state:
            return ''
        v = state[n]
        v = value_repr(v)
        v = v.replace("'", "\\'")
        v = '='+v
        return v


    g = networkx(rules)
    def data():
        from types import SimpleNamespace as ns
        for ne, d in g.nodes.items():
            yield ns(t='n', ne=ne, d=d) #
        for ne, d in g.edges.items():
            yield ns(t='e', ne=ne, d=d)

    def parts():
        def type(n):
            _ = g.nodes[n][terms.types.type]
            return _

        for d in data():
            # nodes
            if d.t == 'n':
                yield part(d.ne, d.d['type'] )
            else:# edges
                assert(d.t == 'e')
                src, dst = d.ne
                st, dt = type(src), type(dst)
                if d.d[terms.types.type] == terms.types.f.binding.input:
                    yield f"{part(src, st)}-->{part(dst, dt )}"
                #if d.d[terms.types.type] == terms.types.f.binding.input:
                #    yield f"{part(src, st)}-->"{part(dst, dt )}"

        # if isinstance(r, data.Block):
        #     block = r
        #     for o in block.oz:
        #         yield f"{part((block.f), 'f')}-->{part(o, 'o')}"
        #     if not block.iz:
        #         yield part((block.f), 'f')
        # elif isinstance(r, data.VarMap):
        #     vm = r
        #     yield f"{part(vm.state_key, 's')}-->{part(vm.arg, 'i')}{part(vm.f, 'f')}"
        # elif isinstance(r, data.State):
        #     if not rules.funcs:
        #         yield f"{part(r.k, 's')}"
        # else:
        #     assert(isinstance(r, _Rules))
        #     for d in r.data():
        #         yield from parts(d)
    
    _ = parts()
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
