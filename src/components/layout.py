from dash import Dash, html

from . import range_dropdown, line_chart, data_dropdown, modal
from ..mortgage_data import TotalPaymentRecord


def create_layout(app: Dash, data: TotalPaymentRecord) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    range_dropdown.render(app),
                    data_dropdown.render(app),
                    modal.render(app, data.mortgage_list),
                ],
            ),
            line_chart.render(app),
        ],
    )
