import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    from state_rules import Rules
    rs = Rules({'x':3, 'xx': 55, }, log=True)

    #@rs.register()
    def f(x): return str(x)+'f'
    _ = rs.register_func(f, {'return': ()} )
    _ = rs.register_func(f, {'x':'x',    } )
    #_ = rs.register_func(f, {'x':'x',  'return': 'f[1]'  } )
    print(_)
    #@rs.register({'x': 'y', 'return': () }, )
    #def pass_(x): return x


    @rs.register({'x': 'f[1]' })
    def ff(x): ...
    #rs.register
    #rs()
    import marimo as mo
    _ = rs.mermaid()
    _ = mo.mermaid(_)
    print(rs.io)
    _
    return Rules, mo, rs


@app.cell
def _(rs):
    import state_rules.struct.graph as sg
    _ = sg.networkx(rs)
    #_ = rs.graph()
    #_ = [(_).nodes, _.edges]
    list(_.nodes.items())
    return (sg,)


@app.cell
def _(mo, rs, sg):
    rs()
    _ = sg.mermaidnx(rs)
    print(_)
    _ = mo.mermaid(_)
    _
    return


@app.cell
def _(Rules):
    rs2 = Rules({'x':(33,3)})
    #@rs2.register
    def f2(x): return 'xxxx'
    @rs2.register({'return': 'g'})
    def g(x): return ('g','3')
    @rs2.register({'x': 'g'})
    def h(x): return

    #_ = rs2+rs
    _ = rs2
    #_.run()
    #print(_.mermaid())
    _
    return (rs2,)


@app.cell
def _(rs2):
    rs2.io
    return


if __name__ == "__main__":
    app.run()
