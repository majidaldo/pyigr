import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import pyigr.connecting as c
    fs = c.Connecting(name='test')
    @fs.register({
        'x': 'x',
         'y': 'x',
        'return': ('f1', 'f2' ),
    })
    def f(x, y, *, z=9):
        #return  {'k':x+y, 'ff': x}
        return {'x': (x,y,z), 'r': x+y+z }

    def ff(): ...

    fs.fmaps[0].fname

    return (fs,)


@app.cell
def _(fs):
    import pyigr.vis.mermaid as vm
    _ = vm.flowchart(fs)
    _ = str(_)
    #print(_)
    import marimo as mo
    _ = mo.mermaid(_)
    _
    return


if __name__ == "__main__":
    app.run()
