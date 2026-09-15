import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import state_rules.struct.graph as sg
    from state_rules import Rules


    rs = Rules({'x':3}, log=True)


    #@rs.register({'return': NO_RETURN })
    def f(x): return 'sdfsd'
    rs.register_func(f, {'return': ()} )
    rs.register_func(f, {'return': ('y', 'z') } )

    @rs.register
    def ff(x): ...
    #rs.register
    _ = sg.mermaid(rs)
    print(_)
    import marimo as mo
    rs.run(2)
    rs
    return (rs,)


@app.cell
def _(rs):
    rs.log
    return


if __name__ == "__main__":
    app.run()
