import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import state_rules.rules as rm
    _r = rm.Rules({'x':1}, log=True)
    @_r.register({
        'x': 'x',
         'y': 'x',
        'return': 'x',
    })
    def _f(x, y,):
        return x+y

    _r.run(5, )
    _r.log
    return (rm,)


@app.cell
def _(rm):
    # return to state
    _r = rm.Rules({'x':1}, log=True)
    @_r.register({
        'x': 'x',
         'y': 'x',
        'return': {'const':'abc'}})
    def _f(x, y,):
        _ = {'a': 1, 'b': 2, 'c': 3, 'r': x+y, }
        _['x'] = x+y
        _['y'] = x+y+1
        return _

    _r.run(5,)
    _r.log
    return


@app.cell
def _(rm):
    # case for 'flexible' argmaps
    from box import Box
    # Instantiate the same ways as a regular dict
    _s = Box({
    'x':{'x': 1},
    'z.y.x' : 3,
    'y': ['yv'],
    },
        default_box=True, box_dots=True)
    _s = dict(_s.items(dotted=True))
    _r = rm.Rules(_s, log=True)
    # second argmap
    @_r.register({'x': 'z.y.x', 'return': 'z.y.x.r' })
    # first argmap
    @_r.register({'x': 'x.x', 'return': 'x.x.r' })
    def fd(x): return x+x

    _r.run(9)
    print(*_r.log, sep='\n')
    Box(_r.state,
        default_box=True, box_dots=True)
    return


if __name__ == "__main__":
    app.run()
