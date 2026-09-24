from dask.dot import label
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
    @classmethod
    def remnl(cls, s: str, sep=''):
        return s.replace('\n',sep)

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
            _ = (
            '---',
            f'title: {_}',
            '---')
        else:
            _ = ''
        return _

    def __str__(self):
        _ = self.title
        _ = _+ (f'flowchart {self.orient}',)
        _ = _ + tuple(self.nodes())
        _ = _ + tuple(self.edges())
        _ = strops.strip(_)
        return _
    
    @classmethod
    def repr(cls, o):
        for n in ('name', 'label', ):
            if not isinstance(n, dict):
                if hasattr(o, n):
                    return getattr(o, n)
            else:
                if n in o:
                    return o[n]
        return str(o)

    
    from ..connecting import Graph
    terms = Graph.terms
    del Graph
    def nodes(self):
        terms = self.terms
        for i, n in enumerate(self.graph.nodes):
            # i more stable than id? id=str(n)+str(i) but then have to coordinte with edges()
            mid = str(id(n))
            label=self.repr(self.graph.nodes[n][terms.label])
            label = label if label else ''
            label = '"'+label+'"' # quote to avoid interpreting
            type = self.graph.nodes[n][terms.types.type]
            if type == self.terms.types.variable.variable:
                yield (f"{mid}"
                    f'@{{shape: stadium, label: {label}}}')
            elif type ==  self.terms.types.f.function:
                yield (f"{mid}"
                    f'[\\{label}/]')
            elif type == self.terms.types.f.arg:
                yield (f"{mid}"
                    f'@{{shape: flip-tri, label: {label}}}')
            else: # shouldnt be here
                yield f"{mid}"

    def edges(self):
        for s,d in self.graph.edges:
            yield f'{id(s)}-->{id(d)}'

def flowchart(con: Connecting, **kw):
    assert(isinstance(con, Connecting))
    _ = FlowChart(con, **kw)
    return _        

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


