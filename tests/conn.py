import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    import marimo as mo
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
    @fs.register({'return': { 'args': 'args', 'r':'r' } })
    def ff(x,y, *, z=9):
        #return  {'k':x+y, 'ff': x}
        return {'args':(x,y), 'r': x+y+z}
    @fs.register({ 'r': 'r' })
    def g( r): return  r
    _ = fs.execs.state({'x':3,'y': 4  })
    #_ = fs.fmaps[0]({'x':3,'y': 4  })
    #_ = fs.fmaps[0].returns(_)
    #fs.fmaps[0].o,
    #_ = fs
    print(*fs.fmaps, sep='\n')
    _
    return (fs,)


@app.cell
def _(fs):
    import pyigr.struct.composition as gc
    _ = gc.compose(fs.fmaps[0].f, fs.fmaps[1].f)
    #_ = _.execs.state({'x':3,'y':5})
    _
    return


@app.cell
def _(fs):
    import pyigr.struct.set as pa
    fs.sets
    return


@app.cell
def _(fs):
    _ = fs.sets.hom
    _
    return


if __name__ == "__main__":
    app.run()
