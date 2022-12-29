from typing import Protocol
from dash import html
from . import ids


class PaymentRecord(Protocol):
    def payment_this_month(self) -> float:
        ...

    def starting_principle_this_month(self) -> float:
        ...

    def ending_principle_this_month(self) -> float:
        ...


def render(data: PaymentRecord) -> html.Div:
    header = f"Payments Owed This Month: €{data.payment_this_month():,.2f}"
    subhead = f"This will reduce the principle from €{data.starting_principle_this_month():,.2f} to €{data.ending_principle_this_month():,.2f}"
    return html.Div(
        [html.H4(header), html.H6(subhead)],
        id=ids.CURRENT_MONTH_PAYMENT,
        style={
            "border": "2px solid black",
            "flex": 1,
            "padding": 25,
        },
    )
