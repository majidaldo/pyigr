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
    return c, fs


@app.cell
def _(fs):
    import pyigr.struct.set as ps
    S  =ps.types.Set
    _ = fs
    _ = _.sets
    _ = _.hom
    #_ = _[S({'0x'}), S({'g2',})]  #{'xx':3,'yy':5} }
    _
    return


@app.cell
def _(fs2):

    _ = fs2.sets
    _ = _.partials
    #_ = _.hom
    #_ = _(S(''))
    #print(_.partials({S('xyf'): {'x':1, 'y':11, 'f': 33 }}))
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
