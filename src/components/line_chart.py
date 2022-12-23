from datetime import datetime
from dash import Dash, dcc, html
import plotly.express as px
from dash.dependencies import Output, Input
from src.mortgage_data import TotalPaymentRecord, PaymentSchema
from . import ids

m = TotalPaymentRecord()
mortgage = m.calculate_payments()


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.LINE_CHART, "children"),
        [
            Input(ids.PLOT_RANGE_DROPDOWN, "value"),
            Input(ids.DATA_TYPE_DROPDOWN, "value"),
        ],
    )
    def update_line_graph(range: str, type: str) -> html.Div:
        if range == "Only Past":
            data = mortgage[mortgage.index <= datetime.today()]
        elif range == "Mortgage Agreements":
            data = mortgage[mortgage[PaymentSchema.mortgage_name] != "Future"]
        else:
            data = mortgage

        fig = px.line(
            x=data.index,
            y=data[type],
            markers=True,
            title=type,
            color=data[PaymentSchema.mortgage_name],
        )
        return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART)

    return html.Div(id=ids.LINE_CHART)
