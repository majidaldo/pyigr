import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import state_rules.struct.graph as sg
    from state_rules import Rules, NO_RETURN


    rs = Rules({'x':3}, log=True)


    #@rs.register({'return': NO_RETURN })
    def f(x): return 'sdfsd'
    rs.register_func(f,  )
    rs.register_func(f, {'return': ('y', 'z') } )

    #rs.register
    _ = sg.mermaid(rs)
    print(_)
    import marimo as mo
    mo.mermaid(_)
    return (rs,)


@app.cell
def _(rs):
    rs.run()
    rs.log
    return


if __name__ == "__main__":
    app.run()
