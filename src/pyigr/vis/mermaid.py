try: from icecream import ic
except: ImportError

from ..connecting import Connecting


class strops:
    @classmethod
    def strip(cls, lines):
        _ = lines
        _ = (l for l in _ if l)
        _ = (l.strip() for l in _)
        _ = '\n'.join(_)
        return _

class FlowChart:
    def __init__(self,
            con: Connecting= Connecting(),
            orient = 'TD',
            ) -> None:
        self.con = con
        self.orient = orient
    
    @property
    def graph(self): return self.con.graph

    @property
    def title(self):    
        if self.con.name:
            _ = f"{self.con.name}"
        else:
            _ = str(self.con)
        _ = (
        '---',
        f'title: {_}',
        '---')
        return _

    def __str__(self):
        _ = self.title
        _ = _+ (f'flowchart {self.orient}',)
        _ = strops.strip(_)
        return _
    
    def nodes(self):
        #for n in self.graph.nodes:
        ...


def flowchart(con: Connecting, **kw):
    assert(isinstance(con, Connecting))
    _ = FlowChart(con, **kw)


    def repr(o):
        for n in {'name', 'label', }:
            if hasattr(o, n):
                return getattr(o, n)
        return str(o)
        

    from ..connecting import Graph
    terms = Graph.terms
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


