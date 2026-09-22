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
    def f(x, y,*, z=0):
        #return  {'k':x+y, 'ff': x}
        return x+y

    fm = {'x': 'xx', 'y':'yy', 'return': ('r','rr') }
    cf = c.F.from_fmap(f,fm)
    def argmap(fm): return {k:v for k,v  in fm.items() if k!='return'}
    am = argmap(fm)
    _ = cf({'xx': 3, 'yy': 3, 'kk':0}, am  )
    cf.returns(_, )
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
