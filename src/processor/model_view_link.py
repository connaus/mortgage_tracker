from dash import Dash, Output, Input, State, html, dcc
import plotly.express as px

from components import ids
from datetime import date, datetime
from data.mortgage_data import TotalPaymentRecord, PaymentSchema


class Updater:
    def __init__(self, app: Dash, data: TotalPaymentRecord) -> None:
        self.app = app
        self.data = data

    def run(self):
        @self.app.callback(
            Output(ids.LINE_CHART, "children"),
            [
                Input(ids.PLOT_RANGE_DROPDOWN, "value"),
                Input(ids.DATA_TYPE_DROPDOWN, "value"),
                Input(ids.MORTGAGE_EDIT_MODAL_CLOSE, "n_clicks"),
            ],
            [
                State(ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS, "n_clicks"),
                State(ids.MORTGAGE_AGREEMENT_MODAL_NEXT, "n_clicks"),
                State(ids.MORTGAGE_EDIT_MODAL_NAME, "value"),
                State(ids.MORTGAGE_EDIT_MODAL_RATE, "value"),
                State(ids.MORTGAGE_EDIT_MODAL_START, "date"),
                State(ids.MORTGAGE_EDIT_MODAL_FIXED_TERM_YEARS, "value"),
                State(ids.MORTGAGE_EDIT_MODAL_FIXED_TERM_MOTHS, "value"),
                State(ids.MORTGAGE_EDIT_MODAL_TERM_YEARS, "value"),
                State(ids.MORTGAGE_EDIT_MODAL_TERM_MOTHS, "value"),
                State(ids.MORTGAGE_EDIT_MODAL_PRINCIPLE, "value"),
            ],
        )
        def update_line_graph(
            range: str,
            type: str,
            n1: int,
            prev: int,
            next: int,
            name: str,
            rate: float,
            start_date: date,
            fixed_years: int,
            fixed_months: int,
            term_years: int,
            term_months: int,
            principle: float,
        ) -> html.Div:
            mortgage = self.data.mortgage_list[next - prev]
            if n1:
                if name:
                    mortgage.mortgage_name = name
                if rate:
                    mortgage.interest_rate = rate / 100
                if start_date:
                    mortgage.start_date = start_date
                if fixed_years or fixed_months:
                    mortgage.fixed_term = (fixed_years * 12) + fixed_months
                if term_years or term_months:
                    mortgage.term = (term_years * 12) + term_months
                if principle:
                    mortgage.principle_at_start = principle

            record = self.data.payment_record
            if range == "Only Past":
                plot_data = record[record.index <= datetime.today()]
            elif range == "Mortgage Agreements":
                plot_data = record[record[PaymentSchema.mortgage_name] != "Future"]
            else:
                plot_data = record

            fig = px.line(
                x=plot_data.index,
                y=plot_data[type],
                labels={"x": "Date", "y": type},
                markers=True,
                title=type,
                color=plot_data[PaymentSchema.mortgage_name],
            )
            return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART)

        return html.Div(id=ids.LINE_CHART)
