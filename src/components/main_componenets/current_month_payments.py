from dash import html
from .. import ids
from processor.model_view_link import Updater


def render(data: Updater) -> html.Div:
    header, subhead = data.current_month_payment_text()
    return html.Div(
        [html.H4(header), html.H6(subhead)],
        id=ids.CURRENT_MONTH_PAYMENT,
        style={
            "border": "2px solid black",
            "flex": 1,
            "padding": 25,
        },
    )
