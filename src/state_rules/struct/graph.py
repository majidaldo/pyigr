from ..rules import Rules as _Rules, Data as data

class Rules(_Rules):
    def mermaid(self, log_idx=-1):
        return mermaid(self, log_idx=log_idx)
    
    def _display_(self):
        _ = mermaid(self)
        from marimo import mermaid as md
        _ = md(_)
        return _


def networkx(rules: _Rules):
    from networkx import DiGraph
    _ = DiGraph()
    rd = rules.graph()
    _.add_nodes_from(rd.nodes.items())
    # cant add directly??
    #_.add_edges_from(rd.edges)
    for s in rd.edges:
        for d in rd.edges[s]:
            _.add_edge(s, d, **rd.edges[s][d] if rd.edges[s][d] else {})
    return _


def frepr(f):
    try:
        f = f.f
    except:
        f = f
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
    ml = 20
    if len(_)>ml:
        _ = _[:ml]
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
    from functools import cache
    @cache
    def part(n, type, id=id, ):
        v = val
        if type == 'f':
            return f"{type}{id(n)}[\\{ frepr(n) }/]"
        if type in {'s', 'o'}:
            return f'so{id(n)}@{{shape: stadium, label: "{frepr(n)+val(n, type, )}" }}'
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
        v = v.replace("'", "\\'")
        v = '='+v
        return v

    def parts(r: data.Block | data.VarMap | _Rules):
        if isinstance(r, data.Block):
            block = r
            for o in block.oz:
                yield f"{part((block.f), 'f')}-->{part(o, 'o')}"
            if not block.iz:
                yield part((block.f), 'f')
        elif isinstance(r, data.VarMap):
            vm = r
            yield f"{part(vm.state_key, 's')}-->{part(vm.arg, 'i')}{part(vm.f, 'f')}"
        elif isinstance(r, data.State):
            if not rules.funcs:
                yield f"{part(r.k, 's')}"
        else:
            assert(isinstance(r, _Rules))
            for d in r.data():
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
    


def mermaidnx(rules: Rules, log_idx=-1):
    if log_idx == -1 and (len(rules.log)==0):
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
    from functools import cache
    @cache
    def part(n, type, id=id, ):
        v = val
        if type == 'f':
            return f"{type}{id(n)}[\\{ frepr(n) }/]"
        if type in {'s', 'o'}:
            return f'so{id(n)}@{{shape: stadium, label: "{frepr(n)+val(n, type, )}" }}'
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
        v = v.replace("'", "\\'")
        v = '='+v
        return v

    def parts(r: data.Block | data.VarMap | _Rules):
        if isinstance(r, data.Block):
            block = r
            for o in block.oz:
                yield f"{part((block.f), 'f')}-->{part(o, 'o')}"
            if not block.iz:
                yield part((block.f), 'f')
        elif isinstance(r, data.VarMap):
            vm = r
            yield f"{part(vm.state_key, 's')}-->{part(vm.arg, 'i')}{part(vm.f, 'f')}"
        elif isinstance(r, data.State):
            if not rules.funcs:
                yield f"{part(r.k, 's')}"
        else:
            assert(isinstance(r, _Rules))
            for d in r.data():
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
