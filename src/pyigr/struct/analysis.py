
def dataclass(c):
    from dataclasses import dataclass
    return dataclass(frozen=True)(c)


from ..connecting import Connecting, types as ctypes
class Analysis:
    def __init__(self, con: Connecting):
        self.con = con

    def paths(self):
        ...

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
                o = ctypes.IO(o),
            )

    # @property
    # def fmap(self):
    #     """return the whole thing like a func""" 
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
