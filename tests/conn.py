import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    play around with the functions here to make sure they make sense
    """)
    return


@app.cell
def _():
    import pyigr.connecting as c
    fs = c.Connecting(name='test')
    {
        'x': 'x',
         'y': 'x',
        'return': ('f1', 'f2' ),
    }
    @fs.register
    def ff(x, y, *, z=9):
        #return  {'k':x+y, 'ff': x}
        return {'x': (x,y,z), 'r': x+y+z }

    def f(x): ...
    #fs.add_func(f)
    #fs.add_func(ff, {})

    #@fs.register({'return':()})
    def g(y): None
    #fs.add_func(g, {'y': 'f0'})
    fs
    return (fs,)


@app.cell
def _(fs):
    import pyigr.struct.analysis as pa
    fs.analysis.con
    return (pa,)


@app.cell
def _(fs, pa):
    _ = fs.analysis.con.fmaps[0]
    _ = _({ pa.ctypes.Set({'x','y'}) :{'x':3, 'y':5 }})
    _
    return


if __name__ == "__main__":
    app.run()
