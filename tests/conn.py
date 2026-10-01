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
    @fs.register({ 'r': 'r', 'rr': 'args' })
    def g(rr, r): return  r,rr
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
    _ = {'0y':22, '0x':11,}
    #_ = fs.fmaps[0](**_)#, fs(_)
    _ =fs(_)
    #fs.fmap.conn
    from inspect import signature as sig
    #_ = sig(_)#.f)
    _
    return


@app.cell
def _(fs):
    import pyigr.struct.composition as gc
    #_ = gc.compose(fs.fmaps[0].f, fs.fmaps[1].f)
    _ = gc.compose(fs.fmaps[0], fs.fmaps[1])
    _ = _#({ '0x': 55, '0y':5, })
    print(_.fmaps[1].iomap)
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
