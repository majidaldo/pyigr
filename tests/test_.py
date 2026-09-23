import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import pyigr.connect as c
    fs = c.Connect(name='test')
    @fs.register({
        'x': 'x',
         'y': 'x',
        'return': 'f',
    })
    def f(x, y, *, z=9):
        #return  {'k':x+y, 'ff': x}
        return {'x': (x,y,z), 'r': x+y+z }

    iom = {'x': 'xx',  'y':'yy',  'return': ('r', 'x' ) }
    fm = c.FMap.from_iomap(f,iom)
    #_ = cf({'xx': 5, 'yy': 8, 'zz': 1, 'extra':'words'}, am)
    _ = fm({'yy': 10, 'xx': 11},  )

    return (fs,)


@app.cell
def _(fs):
    fs.funcs
    return


if __name__ == "__main__":
    app.run()
