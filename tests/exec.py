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
def _(sdf):
    from reaktiv import signal, computed
    from pyigr.exec.state import ComputeSignal
    from reaktiv import ComputeSignal

    # Base signals
    x = signal(0)
    y = signal(2)

    # Computed signal using decorator
    @computed # this is a signal
    def inc():
        #try:
        _ = x() + 1# y()
        #except: return x()
        print(_)
        return _

    def inc():
        for i in range(10):
            _ = inc()
            try:
                sdf
                _ = inc()
                print(i,_)
            except RecursionError:
                print(i,'re')
                #_ = inc() cant do this
                #print(_)


    r = inc()
    print(r)
    return


if __name__ == "__main__":
    app.run()
