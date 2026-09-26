import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    from pyigr import Connecting as C
    fs = C()

    # try edge cases
    @fs.register
    def f(x,y): return x+11+y
    #@fs.register({'x':'x', 'return':'f0' })
    #def ff(x):  return 3
    #fs.add_func(f, { 'x':'f0', 'return':'ffff' }  )
    #fs.add_func(f, { 'x':'f0', 'return': 'ff' }  )
    print(fs.fmaps[0].i)
    fs
    return (fs,)


@app.cell
def _(fs):
    s = {'y': 0, 'x': 11,  **dict.fromkeys(range(5)) }
    _ = fs.execs
    _ = _.state.run(s, log=True)
    _, _.state, _.log

    return


if __name__ == "__main__":
    app.run()
