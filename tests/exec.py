import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    from pyigr import Connecting as C
    fs = C()

    @fs.register({'return': 'x' })
    def f(x): return x+1
    #@fs.register({'x':'x', 'return':'f0' })
    #def ff(x): return 3
    #fs.add_func(f, { 'x':'f0', 'return':'ffff' }  )
    #fs.add_func(f, { 'x':'f0', 'return': 'ff' }  )
    fs
    return (fs,)


@app.cell
def _(fs):
    s = {'y': 0, 'x': 33}
    _ = fs.execs
    _.state.run(s,  log=True).log
    return


if __name__ == "__main__":
    app.run()
