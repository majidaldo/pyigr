import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    from pyigr import Connecting as C
    fs = C()
    @fs.register
    def f(x): return x+1
    #@fs.register
    #def ff(x): return 3
    fs.add_func(f, {'return': 'f0',  }  ) # is this ok?? TODO
    print(fs)
    fs
    return (fs,)


@app.cell
def _(fs):
    import pyigr.exec.state as ps
    s = {'x': 3}
    r = ps.Run(fs)
    _ = r._onepass(s)
    list(_) 
    return


if __name__ == "__main__":
    app.run()
