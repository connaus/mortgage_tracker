from dash import Dash, html

from . import (
    range_dropdown,
    line_chart,
    data_dropdown,
    payment_totals,
    interest_payment_totals,
)
from ..mortgage_data import TotalPaymentRecord


def create_layout(app: Dash, data: TotalPaymentRecord) -> html.Div:
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
            html.Div(
                [
                    payment_totals.render(app, data),
                    interest_payment_totals.render(app, data),
                ],
                style={"display": "flex", "flex-direction": "row"},
            ),
        ],
    )
