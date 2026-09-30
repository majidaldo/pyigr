try: from icecream import ic
except ImportError: pass

from ..connecting import Connecting
class Execs:
    def __init__(self,
            conn: Connecting,
            inits = {},
                 ) -> None:
        self.conn = conn
        self.inits = inits

    def __repr__(self) -> str:
        return 'Executors:'+','.join(self.list)

    def kwargs(self, exec):
        if exec in self.inits:
            return self.inits[exec]
        else:
            return {}

    list = {'state',}
    from functools import cached_property
    @cached_property
    def state(self):
        from ..exec.state import Run
        _ = Run(self.conn, **self.kwargs('state'))
        return _

    def __iter__(self):
        for an in dir(self):
            if an in self.list:
                yield getattr(self, an)
