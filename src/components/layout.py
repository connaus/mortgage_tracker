from dash import Dash, html

from . import (
    range_dropdown,
    line_chart,
    data_dropdown,
    edit_mortgage_modal,
    view_mortgage_modal,
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
                children=[
                    range_dropdown.render(app),
                    data_dropdown.render(app),
                    view_mortgage_modal.render(app, data.mortgage_list),
                    edit_mortgage_modal.render(app, data),
                ],
            ),
            line_chart.render(app),
        ],
    )
