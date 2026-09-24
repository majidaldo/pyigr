# put assertions about a graph here

from ..connecting import Connecting
def no_cycles(con: Connecting):
    raise NotImplementedError



    # def _chk_binding(self):
    #     returns = set()
    #     for fm in self.funcs:
    #         returns.update(fm.return_statekeys)
    #     for fm in self.funcs:
    #         for a,sk in fm.argmap.items():
    #             if          (sk in self.state) or (sk in returns): ...
    #             else: raise KeyError(f'{fm.f.name}{a} will not be bound.')
    # def _chk_flow(self):
    #     # no circles
    #     # chk distinct inputs outputs
    #     ...
