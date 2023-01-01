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

from processor.model_view_link import Updater


def create_layout(updater: Updater) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(updater.app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    range_dropdown.render(updater.app),
                    data_dropdown.render(updater.app),
                    view_mortgage_modal.render(updater.app),
                    edit_mortgage_modal.render(updater.app),
                ],
            ),
            line_chart.render(updater.app),
            html.Div(
                [
                    current_month_payments.render(updater),
                    payment_totals.render(),
                    interest_payment_totals.render(),
                ],
                style={"display": "flex", "flex-direction": "row"},
            ),
        ],
    )
