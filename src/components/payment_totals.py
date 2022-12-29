from typing import Protocol
from dash import Dash, html, Output, Input
from . import ids


class PaymentRecord(Protocol):
    def payment_to_date(self) -> float:
        ...

    def principle_reduction_to_date(self) -> float:
        ...

    def payment_agreed(self) -> float:
        ...

    def principle_reduction_agreed(self) -> float:
        ...

    def cost_of_mortgage(self) -> float:
        ...

    def perc_mortgage_paid(self) -> float:
        ...


def render(app: Dash, data: PaymentRecord) -> html.Div:
    @app.callback(
        Output(ids.TOTAL_PAYMENTS, "children"),
        Input(ids.PLOT_RANGE_DROPDOWN, "value"),
    )
    def update_payment_text(range: str) -> list[html.H4 | html.H6]:
        if range == "Only Past":
            header = f"Payments to Date: €{data.payment_to_date():,.2f}"
            subhead = (
                f"Reduction in Principle: €{data.principle_reduction_to_date():,.2f}"
            )
        elif range == "Mortgage Agreements":
            header = f"Payments Agreed: €{data.payment_agreed():,.2f}"
            subhead = f"Reduction in Principle Agreed: €{data.principle_reduction_agreed():,.2f}"
        else:
            header = f"Cost of Mortgage: €{data.cost_of_mortgage():,.2f}"
            subhead = (
                f"Percentage of Mortgage Paid: {data.perc_mortgage_paid() * 100:.1f}%"
            )
        return [html.H4(header), html.H6(subhead)]

    header = f"Payments to Date: €{data.payment_to_date():,.2f}"
    subhead = f"Reduction in Principle: €{data.principle_reduction_to_date():,.2f}"
    return html.Div(
        [html.H4(header), html.H6(subhead)],
        id=ids.TOTAL_PAYMENTS,
        style={
            "border": "2px solid black",
            "flex": 1,
            "padding": 25,
        },
    )
