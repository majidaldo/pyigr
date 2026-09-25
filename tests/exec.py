import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    from pyigr import Connecting as C
    fs = C()

    @fs.register
    def f(x): return x+1
    @fs.register({'x':'y'})
    def ff(x): return 3
    #fs.add_func(ff, {'x':'z', 'return':'f0' }  ) 
    fs
    return (fs,)


@app.cell
def _(fs):
    import pyigr.exec.state as ps
    s = {'y': 0}
    r = ps.Run(fs)

    _ =r.run(s, log=True)
    _.state
    return


if __name__ == "__main__":
    app.run()
