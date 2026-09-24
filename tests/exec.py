import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", auto_download=["html"])


app._unparsable_cell(
    r"""
    from pyigr.connecting
    rs = Rules({'x':3, 'xx': 55, }, name='test', log=True)
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
