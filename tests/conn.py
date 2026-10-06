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
    fs.add_func(g, {'r':'r1', 'x':'r1', 'return': 'g2' })
    _ = fs
    _
    return (c,)


@app.cell
def _(fs2):
    import pyigr.struct.set as ps
    S  =ps.types.Set
    _ = ps.varsafter(fs2.sets.conn)
    _ = _({S({'xx', 'yy'}): {'xx':3,'yy':5} }  )
    _
    return


@app.cell
def _(fs2):

    _ = fs2.sets
    _ = _.partials
    #_ = _.hom
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
    return (fs2,)


if __name__ == "__main__":
    app.run()
