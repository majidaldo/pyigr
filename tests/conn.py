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
    return (c,)


@app.cell
def _(c):
    fs2 = c.Connecting()

    def f2(x): return 555
    fs2.add_func(f2, {'return': ('a','b','c') })
    #_ = fs2({'x':3})
    _ = fs2
    _
    return (fs2,)


@app.cell
def _(fs2):
    import types
    _ = fs2.paths
    #_ =_({c.types.Set({'x'}): 3,  } )
    #_ =_({'x': 3 } )
    #print(_)
    _.fmaps[0].f({'x':5})
    return


if __name__ == "__main__":
    app.run()
