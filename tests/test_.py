import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import pyigr.connect as c
    fs = c.Connect(name='test')
    @fs.register({
        'x': 'x',
         'y': 'x',
        'return': ('f1', 'f2' ),
    })
    def f(x, y, *, z=9):
        #return  {'k':x+y, 'ff': x}
        return {'x': (x,y,z), 'r': x+y+z }

    def ff(): ...

    fs.register_func(ff,  )
    #_ = fs.funcs[1]({'x': 10, 'y': 11} ,  )
    fs.funcs[0]
    return (fs,)


@app.cell
def _(fs):
    print(*fs.graph.edges, sep='\n')
    return


if __name__ == "__main__":
    app.run()
