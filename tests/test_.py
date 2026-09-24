import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import pyigr.connecting as c
    fs = c.Connecting(name='test')
    {
        'x': 'x',
         'y': 'x',
        'return': ('f1', 'f2' ),
    }
    def ff(x, y, *, z=9):
        #return  {'k':x+y, 'ff': x}
        return {'x': (x,y,z), 'r': x+y+z }

    def f(x): ...
    fs.add_func(f)
    fs.add_func(ff, {'return':'y'})

    print(*fs.graph.edges, sep='\n')
    return (fs,)


@app.cell
def _(fs):
    import pyigr.vis.mermaid as vm
    fs
    return


if __name__ == "__main__":
    app.run()
