import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    from state_rules import Rules
    rs = Rules({'x':3, 'xx': 55, }, name='test', log=True)

    #@rs.register()
    def f(x): return x
    #_ = rs.register_func(f, {'return': ()} )
    _ = rs.register_func(f, {'x':'x', 'return': 'f[0]'   } )
    _ = rs.register_func(f, {'x':'f[0]', 'return': 'f[0]'  } )
    #@rs.register({'x': 'y', 'return': () }, )
    #d#ef pass_(x): return x

    # bug in mermaid?
    #_ = rs.register_func(f, {'x':'x',    } )
    #_ = rs.register_func(f, {'x':'f[0]', 'return': 'ff'  } )

    #@rs.register({'x': 'f[1]' })
    def ff(x): ...
    #rs.register
    rs()
    import marimo as mo
    _ = rs.mermaid()
    print(_)
    _ = mo.mermaid(_)
    print(rs.io)
    _
    return mo, rs


@app.cell
def _(rs):
    import state_rules.struct.graph as sg
    _ = sg.networkx(rs)
    #_ = rs.graph()
    #_ = [(_).nodes, _.edges]
    list(_.nodes.items())
    return


@app.cell
def _(mo, rs):
    #rs()
    import state_rules.vis.mermaid as rm
    _ = rm.mermaidnx(rs)
    print(_)
    _ = mo.mermaid(_)
    _
    return


if __name__ == "__main__":
    app.run()
