import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import pyigr.exec.state as ps
    from pyigr import Connecting as C
    fs = C()
    @fs.register
    def f(x): return x+1
    fs
    return (ps,)


@app.cell
def _(ps):
    s = ps.States()
    s.update({'x':3})
    s.cur
    return


if __name__ == "__main__":
    app.run()
