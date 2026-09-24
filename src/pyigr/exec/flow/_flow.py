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