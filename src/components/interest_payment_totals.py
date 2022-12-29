from typing import Optional
from dash import Dash, html
from ..mortgage_data import TotalPaymentRecord
from . import ids


def render(app: Dash, data: TotalPaymentRecord) -> html.Div:
    header = f"Total Interest Payments to Date: €{data.total_interest_payment_to_date():,.2f}"
    subhead = f"Percentage of Payments on Interest: {data.perc_interest_payment_to_date() * 100:.1f}%"
    return html.Div(
        [html.H4(header), html.H6(subhead)],
        id=ids.TOTAL_INTEREST_PAYMENTS,
        style={
            "border": "2px solid black",
            "flex": 1,
            "padding": 25,
        },
    )
