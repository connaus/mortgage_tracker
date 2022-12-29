from dash import Dash, html, Output, Input
from . import ids
from typing import Protocol


class PaymentRecord(Protocol):
    def interest_payment_to_date(self) -> float:
        ...

    def perc_interest_payment_to_date(self) -> float:
        ...

    def interest_payment_agreed(self) -> float:
        ...

    def perc_interest_payment_agreed(self) -> float:
        ...

    def total_interest_payment(self) -> float:
        ...

    def total_perc_interest_payment(self) -> float:
        ...


def render(app: Dash, data: PaymentRecord) -> html.Div:
    @app.callback(
        Output(ids.TOTAL_INTEREST_PAYMENTS, "children"),
        Input(ids.PLOT_RANGE_DROPDOWN, "value"),
    )
    def update_payment_text(range: str) -> list[html.H4 | html.H6]:
        if range == "Only Past":
            header = (
                f"Interest Payments to Date: €{data.interest_payment_to_date():,.2f}"
            )
            subhead = f"Percentage of Payments on Interest: {data.perc_interest_payment_to_date() * 100:.1f}%"
        elif range == "Mortgage Agreements":
            header = f"Interest Payments Agreed: €{data.interest_payment_agreed():,.2f}"
            subhead = f"Percentage of Payments on Interest Agreed: {data.perc_interest_payment_agreed() * 100:.1f}%"
        else:
            header = f"Total Interest Payments: €{data.total_interest_payment():,.2f}"
            subhead = f"Total Percentage of Payments on Interest: {data.total_perc_interest_payment() * 100:.1f}%"
        return [html.H4(header), html.H6(subhead)]

    header = f"Interest Payments to Date: €{data.interest_payment_to_date():,.2f}"
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
