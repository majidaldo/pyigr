from ..connecting import Connecting
class Execs:
    def __init__(self, conn: Connecting) -> None:
        self.conn = conn

    def __repr__(self) -> str:
        return 'Executors:'+','.join(self.list)

    list = {'state',}
    @property
    def state(self):
        from ..exec.state import Run
        return  Run(self.conn)

    def __iter__(self):
        for an in dir(self):
            if an in self.list:
                yield getattr(self, an)
