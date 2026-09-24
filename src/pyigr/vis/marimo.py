

class Display:
    #from ..connecting import Connecting
    def _display_(self: 'Connecting'):
        from .mermaid import FlowChart
        _ = FlowChart(self)
        _ = str(_)
        from marimo import mermaid
        _ = mermaid(_)
        return _
