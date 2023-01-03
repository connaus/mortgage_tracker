from dash import html, dcc
from .. import ids
from data.mortgage_data import PaymentSchema


def render(style: dict = {}) -> html.Div:
    data_types = [
        PaymentSchema.principle_at_start,
        PaymentSchema.interest_owed,
        PaymentSchema.payment_owed,
        PaymentSchema.actual_payment,
        PaymentSchema.principle_at_end,
        PaymentSchema.overpayment,
    ]
    return html.Div(
        children=[
            html.H6("Data Type"),
            dcc.Dropdown(
                id=ids.DATA_TYPE_DROPDOWN,
                options=[{"label": dtypes, "value": dtypes} for dtypes in data_types],
                value=PaymentSchema.principle_at_start,
                multi=False,
                clearable=False,
            ),
        ],
        style=style,
    )
