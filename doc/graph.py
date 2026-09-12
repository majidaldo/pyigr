import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import state_rules.struct.graph as sg
    from state_rules import Rules, NO_RETURN


    rs = Rules()


    @rs.register({'return': NO_RETURN })
    def f(x): return 'sdfsd'
    #rs.register_func(f,  )
    rs.register_func(f, {'x':f } )

    #rs.register

    _ = sg.mermaid(rs)
    import marimo as mo
    mo.mermaid(_)
    return


if __name__ == "__main__":
    app.run()
