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
    @fs.register({'return': { 'r':'ff', } })
    def ff( y,x, *, z=9):
        #return  {'k':x+y, 'ff': x}
        return {'x': x, 'r': x+y+z }
    @fs.register
    def g(ff): return
    #_ = fs.execs.state({'x':3,'y': 4  })
    #_ = fs.fmaps[0]({'x':3,'y': 4  })
    #_ = fs.fmaps[0].returns(_)
    #fs.fmaps[0].o,
    _ = fs
    print(*fs.fmaps, sep='\n')
    _
    return (fs,)


@app.cell
def _(fs):
    import pyigr.struct.composition as gc
    _ = gc.compose(fs.fmaps[0].f, fs.fmaps[1].f)
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
