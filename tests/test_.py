import marimo

__generated_with = "0.24.2"
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

    _r.funcs
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
