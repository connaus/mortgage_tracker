from dash import Dash, html
from .. import ids


def render(app: Dash) -> html.Div:

    return html.Div(id=ids.LINE_CHART)
