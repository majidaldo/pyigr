import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    #play around with the functions here to make sure they make sense
    return


@app.cell
def _():
    import pyigr.connecting as c
    fs = c.Connecting(name='test')
    _ = {
        'x': '0x',
         'y': '0y',
        'return': { 'args': 'args', 'r':'r' }
    }
    @fs.register(_)
    def ff(x,y, *, z=9):
        #return  {'k':x+y, 'ff': x}
        return {'args':(x,y), 'r': x+y+z}
    @fs.register({ 'r': 'r' })
    def g( r): return  r
    #_ = fs.execs.state({'x':3,'y': 4  })
    #_ = fs({'x':33,'y': 44  })
    #_ = fs.fmaps[0]({'x':3,'y': 4  })
    #_ = fs.fmaps[0].returns(_)
    #fs.fmaps[0].o,
    _ = fs
    print(*fs.fmaps, sep='\n')
    _
    return (fs,)


@app.cell
def _(fs):
    from inspect import signature as s
    _ = {'0y':22, '0x':11, }
    #_ = (fs.fmap).f(_0=11, _1=33)
    #_ = (fs.fmap)
    _ = fs.fmap(_)
    #_ =fs
    #fs.fmap.conn
    #from inspect import signature as sig
    #_ = sig(_.f)
    _
    return


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
