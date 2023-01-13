from dash import html, dcc
from .. import ids


def render(style: dict = {}) -> html.Div:
    plot_range = ["Only Past", "Mortgage Agreements", "Future Projection"]
    return html.Div(
        children=[
            html.H6("Plot Range"),
            dcc.Dropdown(
                id=ids.PLOT_RANGE_DROPDOWN,
                options=[{"label": prange, "value": prange} for prange in plot_range],
                value="Only Past",
                multi=False,
                clearable=False,
            ),
        ],
        style=style,
    )
