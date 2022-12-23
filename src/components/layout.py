from dash import Dash, html

from . import range_dropdown, line_chart, data_dropdown


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[range_dropdown.render(app), data_dropdown.render(app)],
            ),
            line_chart.render(app),
        ],
    )
