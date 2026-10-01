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
    @fs.register({ 'r': 'r', 'rr': 'args', 'return':('r1', 'r2') })
    def g(rr, r): return  r,rr
    #_ = fs.execs.state({'x':3,'y': 4  })
    #_ = fs({'x':33,'y': 44  })
    #_ = fs.fmaps[0]({'x':3,'y': 4  })
    #_ = fs.fmaps[0].returns(_)
    #fs.fmaps[0].o,
    _ = fs
    #print(*fs.fmaps, sep='\n')
    #_({'0y':3, '0x':5 })
    #_ = fs.collapse().collapse().collapse().collapse().collapse()
    #_ = fs.collapse() == _
    #_ = _.expand().expand()
    #_ = _({'0x':5, '0y':55})
    #_ = _.fmaps[0].f.conn.fmaps[0].f.conn.fmaps[0].f.conn.fmaps[0].conn.fmaps[0].conn.fmaps[0].conn
    #from inspect import signature as sig
    #_ = sig(_)
    _
    return c, fs


@app.cell
def _(c):
    fs2 = c.Connecting()

    def f2(x): return 555
    fs2.add_func(f2)
    fs2
    return


@app.cell
def _(fs):
    import pyigr.struct.composition as gc
    _ = gc.compose(fs.fmaps[0].f, fs.fmaps[1].f)
    _ = gc.compose(fs.fmaps[0], fs.fmaps[1])
    #_ = gc.compose(fs, fs)
    #_ = _({ '0x': 55, '0y':5, })
    #_ = gc.compose(fs, fs2)
    _ = gc.compose(lambda x: x, lambda x,y:(x,y) )
    #print(_.fmaps[1].iomap)
    _#.graph.nodes)
    _({'x':3})
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
