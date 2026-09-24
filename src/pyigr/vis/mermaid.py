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
            _ = ('',)
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

