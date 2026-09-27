def dataclass(c):
    from dataclasses import dataclass
    return dataclass(frozen=True)(c)

from ..connecting import Connecting, types as ctypes, FMap

class id:
    def __repr__(self): return self.__class__.__name__
    def __call__(self, i): return i
id = id()


class SetMap: 
    def __init__(self, fm: FMap):
        self.fm = fm
    def __repr__(self):
        return '*'+repr(self.fm)

    def __call__(self, values: dict):
        return self.fm(values)


class Set:
    def __init__(self, con: Connecting):
        self.con = Connecting()
        S = ctypes.Set  # to emphasize
        for fm in con.fmaps:
            # sets -> sets
            self.con.add_func(SetMap(fm), {'values': S(fm.i) , 'return': (S(fm.o),) } ) # interesting...
            self.con.add_func(id, {'i': S(fm.i), 'return': (S(fm.i),) } ) # # interesting nesting
            self.con.add_func(id, {'i': S(fm.o), 'return': (S(fm.o),) } ) # 
            for i in fm.i: self.con.add_func(id, {'i':S({i}),  'return': (S({i}),) } ) 
            for o in fm.o: self.con.add_func(id, {'i':S({o}),  'return': (S({o}),) } )
    

    @property
    def sets(self):
        #for n in self.con.graph.nodes:
        #    if is
        ...

    @property
    def paths(self):
        # not useful to talk about just the vars
        # but sets of them.
        # this is like recovering 
        # serial and parallel  composition?
        inputs =  {fm.i for fm in self.con.fmaps}
        outputs = {fm.o for fm in self.con.fmaps}
        from networkx import all_simple_edge_paths  # to more directly represent composition?
        from networkx import all_simple_paths
        _ = all_simple_paths(self.con.graph, self.con.fmaps[0], self.con.fmaps[2],)
        return _


    @property
    def hom(self):
        ...


    @property
    def io(self):
        """viewing all of con as a func"""
        fins = []
        _ = (fm.i for fm in self.con.fmaps)
        for oz in _: fins.extend(oz)
        fins = frozenset(fins)
        _ = (fm.o for fm in self.con.fmaps)
        fouts = []
        for iz in _: fouts.extend(iz)
        fouts = frozenset(fouts)
        from types import SimpleNamespace as ns
        return self.IO.from_iters(
                i=fins  - fouts,
                o=fouts - fins ) # neat!
    @dataclass
    class IO:
        # like fmap names
        i: ctypes.IO
        o: ctypes.IO
        @classmethod
        def from_iters(cls, i, o):
            return cls(
                i = ctypes.IO(i),
                o = ctypes.IO(o),)

    # @property
    # def fmap(self):
    #     """return the whole thing like a func""" 
    #   maybe put this in composition
    #     ...

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
