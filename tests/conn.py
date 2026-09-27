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

    @fs.register
    def g(ff0): return
    fs
    return (fs,)


@app.cell
def _(fs):
    import pyigr.struct.set as pa
    fs.sets
    return (pa,)


@app.cell
def _(fs, pa):
    _ = fs.sets.con.fmaps[0]
    _ = _({ pa.ctypes.Set({'x','y'}) :{'x':3, 'y':5 }})
    _
    return


@app.cell
def _(fs):
    _ = fs.sets.paths
    _ = list(_)
    _
    return


if __name__ == "__main__":
    app.run()
