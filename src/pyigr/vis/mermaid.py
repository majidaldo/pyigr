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

    from functools import cache
    @staticmethod
    @cache
    def mid(o): #arbitrary obj
        from uuid import uuid4
        return uuid4().hex


    def label(self, n):
        _=self.repr(self.graph.nodes[n][self.terms.label])
        _ = _ if _ else ''
        _ = '"'+_+'"' # quote to avoid interpreting
        return _

    from ..connecting import Graph
    terms = Graph.terms
    del Graph
    def nodes(self):
        terms = self.terms
        for i, n in enumerate(self.graph.nodes):
            label = self.label(n)
            typew = self.graph.nodes[n][terms.types.type]
            if typew == self.terms.types.variable.variable:
                mid = (self.mid(n))
                yield (f"{mid}"
                    f'@{{shape: stadium, label: {label}}}')
            elif typew ==  self.terms.types.f.function:
                mid = self.mid(n)
                yield (f"{mid}"
                    f'[\\{label}/]')
            elif typew == self.terms.types.f.arg:
                continue
            # too noisy and unintended consequeces
            #    yield (f"{mid}"
            #        f'@{{shape: flip-tri, label: {label}}}')
            else: # shouldnt be here
                mid = self.mid(n)
                yield f"{mid}"

    

    def edges(self):
        terms = self.terms
        typew = terms.types.type
        g = self.graph
        def bindings():
            # REF:
            # g.add_edge(var, farg,
            #     **{type: terms.types.f.         binding.binding     })
            # g.add_edge(farg, self,
            #    **{type: terms.types.f.binding. input     })
            # get var --farg---> fmap(self)
            def gn(t):
                for n in g.nodes:
                    if g.nodes[n][typew] == t:
                        yield n
            vs = frozenset(gn(terms.types.variable.variable))
            for var in vs:
                for e1 in g.edges:
                    s,d = e1
                    if s == var:
                        assert(g[s][d][typew]==terms.types.f.binding.binding)
                        farg = d
                        for e2 in g.edges:
                            s,d = e2
                            if s == farg:
                                assert(g[s][d][typew]==terms.types.f.binding.input)
                                fmap = d
                                if var in fmap.i:
                                    yield var, farg, fmap
                    
        for e in g.edges:
            s,d = e
            if g[s][d][typew] in {terms.types.f.binding.output}:
                yield f'{self.mid(s)}-->{self.mid(d)}'
        for s, p, d in frozenset(bindings()):
            yield f'{self.mid(s)}-->|{p.p}|{self.mid(d)}'

