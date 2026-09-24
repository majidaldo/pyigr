import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import pyigr.exec.state as ps
    from pyigr import Connecting as C
    fs = C()
    print(repr(fs)) # not the graph
    return


@app.cell
def _():
    from reaktiv import signal, computed
    from pyigr.exec.state import ComputeSignal
    from reaktiv import ComputeSignal

    # Base signals
    x = signal(10)
    y = signal(20)

    # Computed signal using decorator
    @computed # this is a signal
    def inc():
        #try:
        _ = x() + 1# y()
        #except: return x()
        return _

    def inc():
        for i in range(10):
            try:
                return inc()
            except RecursionError:
                print('re')
                #_ = inc()
                #return _
                ...

    def mycomputed(*p, **k):
        for i in range(10):
            try:
                return computed(*p, **k)
            except:# RuntimeError("Circular dependency detected"):
                print('circular', i)
    #mycomputed = ComputeSignal(inc)



    # Computed value updates automatically
    print(inc())
    return


if __name__ == "__main__":
    app.run()
