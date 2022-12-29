from typing import Optional
from dash import Dash, html
from ..mortgage_data import TotalPaymentRecord
from . import ids


def render(app: Dash, data: TotalPaymentRecord) -> html.Div:
    header = f"Total Payments to Date:\n€{data.total_payment_to_date():,.2f}"
    subhead = f"Total Reduction in Principle:\n€{data.total_principle_reduction():,.2f}"
    return html.Div(
        [html.H4(header), html.H6(subhead)],
        id=ids.TOTAL_PAYMENTS,
        style={
            "border": "2px solid black",
            "flex": 1,
            "padding": 25,
        },
    )
