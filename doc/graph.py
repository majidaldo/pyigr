import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    from state_rules import Rules
    rs = Rules({'x':3, 'xx': 55}, log=True)
    #@rs.register()
    def f(x): return 'sdfsd'
    #rs.register_func(f, {'return': ()} )
    rs.register_func(f, {'return': ('y', 'z'), 'x': 'xx' } )

    #@rs.register
    def ff(x): ...
    #rs.register
    import marimo as mo
    rs.run(5)
    _ = rs.mermaid()
    print(_)
    _ = mo.mermaid(_)
    _
    return Rules, rs


@app.cell
def _(rs):
    import state_rules.struct.graph as sg
    _ = sg.networkx(rs)
    _.nodes
    return


@app.cell
def _(Rules, rs):
    rs2 = Rules({'x':('sdfsdf',3)})
    #@rs2.register
    def f2(x): return 'xxxx'
    @rs2.register
    def g(x): return ('g','3')

    _ = rs2+rs
    #_ = rs2
    _.run()
    print(_.mermaid())
    _
    return


if __name__ == "__main__":
    app.run()
