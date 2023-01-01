from dash import Dash, html
from data.mortgage_data import TotalPaymentRecord
from .. import ids


def render(app: Dash, data: TotalPaymentRecord) -> html.Div:

    return html.Div(id=ids.LINE_CHART)
