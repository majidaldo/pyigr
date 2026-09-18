import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    from state_rules import Rules

    rs = Rules({'x':3, 'y': 33})
    @rs.register({'return': 'f'})
    def f(y, x):
        return x,y
    @rs.register({'return': 'f'})
    def f(y, x):
        return x,y,x,y

    rs
    return (rs,)


@app.cell
def _(rs):
    import state_rules.compile.dask as sc

    sc.test(rs)
    return


if __name__ == "__main__":
    app.run()
