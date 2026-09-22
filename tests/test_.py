import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import pyigr.connect as c
    #_r = c.Connect()
    # @_r.register({
    #     'x': 'x',
    #      'y': 'x',
    #     'return': 'x',
    # })
    def f(x, y, *, z=9):
        #return  {'k':x+y, 'ff': x}
        return {'x': (x,y,z), 'r': x+y+z }

    fm = {'x': 'xx',  'y':'yy',  'return': ('r', 'x' ) }
    cf = c.F.from_fmap(f,fm)
    def argmap(fm): return {k:v for k,v  in fm.items() if k!='return' }
    am = argmap(fm)
    #_ = cf({'xx': 5, 'yy': 8, 'zz': 1, 'extra':'words'}, am)
    _ = cf({'yy': 10, 'xx': 11}, am )
    #_ = cf( (10, 11,), )
    _ = cf.returns(_,)
    _
    return


@app.cell
def _():
    import networkx as nx
    g = nx.DiGraph()
    g.add_node('x', v=3)
    g.nodes._nodes
    return


if __name__ == "__main__":
    app.run()
