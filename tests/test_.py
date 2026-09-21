import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import pyigr.connect as c
    _r = c.Connect()
    # @_r.register({
    #     'x': 'x',
    #      'y': 'x',
    #     'return': 'x',
    # })
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
