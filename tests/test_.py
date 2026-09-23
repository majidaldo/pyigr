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

    fm = fs.register_func(ff,  )
    _ = fs.funcs[0]({'x': 10, 'y': 11} , {0: 'y', 1: 'y' } )
    _ = fs.add(f)
    fs
    return (fs,)


@app.cell
def _(fs):
    print(*fs.graph.edges, sep='\n')
    _ = list(fs.graph.edges)
    fs.graph.edges[_[0]]
    return


if __name__ == "__main__":
    app.run()
