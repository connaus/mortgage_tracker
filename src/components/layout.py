from dash import Dash, html

from components.main_componenets import (
    range_dropdown,
    line_chart,
    data_dropdown,
    payment_totals,
    interest_payment_totals,
    current_month_payments,
)

from components.modals import (
    edit_mortgage_modal,
    view_mortgage_modal,
)

from data.mortgage_data import TotalPaymentRecord


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
            line_chart.render(app, data),
            html.Div(
                [
                    current_month_payments.render(data),
                    payment_totals.render(app, data),
                    interest_payment_totals.render(app, data),
                ],
                style={"display": "flex", "flex-direction": "row"},
            ),
        ],
    )
