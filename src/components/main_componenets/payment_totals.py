from dash import html
from .. import ids


def render() -> html.Div:

    return html.Div(
        [html.H4(), html.H6()],
        id=ids.TOTAL_PAYMENTS,
        style={
            "border": "2px solid black",
            "flex": 1,
            "padding": 25,
        },
    )
