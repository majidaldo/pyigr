import marimo

__generated_with = "0.24.1"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import state_rules.struct.graph as sg
    from state_rules import Rules


    rs = Rules()


    @rs.register()
    def f():...

    rs.add_func(f, {'return': f })

    #rs.register

    _ = sg.mermaid(rs)
    import marimo as mo
    mo.mermaid(_)
    return


if __name__ == "__main__":
    app.run()
