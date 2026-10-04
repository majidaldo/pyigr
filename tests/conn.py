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
        'return': {  'r':'r' }
    }
    @fs.register(_)
    def ff(x, *, z=9):
        #return  {'k':x+y, 'ff': x}
        return {'args':(x,), 'r': x+z}
    @fs.register({ 'r': 'r', 'x':'0x' , 'return':('r1', ) })
    def g(r, x): return  r,x
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
def _(fs):
    import pyigr.struct.set as ps
    S  =ps.types.Set
    _ = fs.sets
    #_ = _.paths
    _ = _.hom
    #_ = _(S(''))
    #print(_.partials({S('xyf'): {'x':1, 'y':11, 'f': 33 }}))
    #_ = _.hom({S('xy'): {'x':3, 'y':33}} )
    #_ = _[S({'0x', '0y'})][S({'r1'})]
    #_ = list(_)
    #_[S('x')]#[S('x')]
    #_ = _.graph.edges#[(S('xy'),S('f'))]
    #_ = _.fmaps#[0]({ S('xy') :   {'f':11, 'y': 22}  } )
    #_  =_#[S({'yy', 'xx'})][S('f')]
    #_  =_[S({'yy', 'xx'})][S('f')]
    #_ = list(_)[0]( {S({'yy', 'xx'}): {'xx':3 , 'yy':5 }} )
    #_ = list(_)
    #_ = list(_(S({ '0x'}), S({'args', 'r'}) )), list(_(S({ 'r', '0x'}), S({'r1', 'r2'}) ))
    #_ = list(_(S({ '0x'}), S({'r1', 'r2'}) ))
    _
    return


@app.cell
def _(c):
    fs2 = c.Connecting()

    def f2(x,y): return 555
    fs2.add_func(f2, {'x':'xx', 'y':'yy',
      'return':'f'} )
    #_ = fs2({'x':3})
    _ = fs2
    _
    return


if __name__ == "__main__":
    app.run()
