import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import state_rules.struct.graph as sg
    Rules = sg.Rules
    rs = Rules({'x':3}, log=True)
    @rs.register()
    def f(x): return 'sdfsd'
    #rs.register_func(f, {'return': ()} )
    #rs.register_func(f, {'return': ('y', 'z') } )

    #@rs.register
    def ff(x): ...
    #rs.register
    import marimo as mo
    rs.run(2)
    _ = rs.mermaid(2)
    _ = mo.mermaid(_)
    _
    return Rules, rs


@app.cell
def _(Rules, rs):
    rs2 = Rules()
    @rs2.register
    def f2(x): return 'xxxx'

    _ = rs2+rs
    _.run()
    _
    return


if __name__ == "__main__":
    app.run()
