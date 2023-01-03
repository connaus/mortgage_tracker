from math import floor
from dash import Dash, Output, Input, State, html, dcc, ctx
import plotly.express as px

from components import ids
from datetime import date, datetime
from data.mortgage_data import TotalPaymentRecord, PaymentSchema, MortgageAgreement


class Updater:
    def __init__(self, app: Dash, data: TotalPaymentRecord) -> None:
        self.app = app
        self.data = data

    def current_month_payment_text(self) -> tuple[str, str]:
        header = f"Payments Owed This Month: €{self.data.payment_this_month():,.2f}"
        subhead = f"This will reduce the principle from €{self.data.starting_principle_this_month():,.2f} to €{self.data.ending_principle_this_month():,.2f}"
        return header, subhead

    def selected_mortgage(self, next: int, prev: int) -> MortgageAgreement:
        return self.data.mortgage_list[next - prev]

    def update_payment_text(self, range: str) -> list[html.H4 | html.H6]:
        if range == "Only Past":
            header = f"Payments to Date: €{self.data.payment_to_date():,.2f}"
            subhead = f"Reduction in Principle: €{self.data.principle_reduction_to_date():,.2f}"
        elif range == "Mortgage Agreements":
            header = f"Payments Agreed: €{self.data.payment_agreed():,.2f}"
            subhead = f"Reduction in Principle Agreed: €{self.data.principle_reduction_agreed():,.2f}"
        else:
            header = f"Cost of Mortgage: €{self.data.cost_of_mortgage():,.2f}"
            subhead = f"Percentage of Mortgage Paid: {self.data.perc_mortgage_paid() * 100:.1f}%"
        return [html.H4(header), html.H6(subhead)]

    def update_interest_text(self, range: str) -> list[html.H4 | html.H6]:
        if range == "Only Past":
            header = f"Interest Payments to Date: €{self.data.interest_payment_to_date():,.2f}"
            subhead = f"Percentage of Payments on Interest: {self.data.perc_interest_payment_to_date() * 100:.1f}%"
        elif range == "Mortgage Agreements":
            header = (
                f"Interest Payments Agreed: €{self.data.interest_payment_agreed():,.2f}"
            )
            subhead = f"Percentage of Payments on Interest Agreed: {self.data.perc_interest_payment_agreed() * 100:.1f}%"
        else:
            header = (
                f"Total Interest Payments: €{self.data.total_interest_payment():,.2f}"
            )
            subhead = f"Total Percentage of Payments on Interest: {self.data.total_perc_interest_payment() * 100:.1f}%"
        return [html.H4(header), html.H6(subhead)]

    def run(self):
        # updates line graph and total boxes when mortgages are added or edited, or drop down selection is changed.
        # TODO: add update to totals
        @self.app.callback(
            [
                Output(ids.LINE_CHART, "children"),
                Output(ids.TOTAL_PAYMENTS, "children"),
                Output(ids.TOTAL_INTEREST_PAYMENTS, "children"),
            ],
            [
                Input(ids.PLOT_RANGE_DROPDOWN, "value"),
                Input(ids.DATA_TYPE_DROPDOWN, "value"),
                Input(ids.MORTGAGE_EDIT_MODAL_CLOSE, "n_clicks"),
                Input(ids.MORTGAGE_ADD_MODAL_CLOSE, "n_clicks"),
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
                State(ids.MORTGAGE_ADD_MODAL_NAME, "value"),
                State(ids.MORTGAGE_ADD_MODAL_RATE, "value"),
                State(ids.MORTGAGE_ADD_MODAL_START, "date"),
                State(ids.MORTGAGE_ADD_MODAL_FIXED_TERM_YEARS, "value"),
                State(ids.MORTGAGE_ADD_MODAL_FIXED_TERM_MOTHS, "value"),
                State(ids.MORTGAGE_ADD_MODAL_TERM_YEARS, "value"),
                State(ids.MORTGAGE_ADD_MODAL_TERM_MOTHS, "value"),
                State(ids.MORTGAGE_ADD_MODAL_PRINCIPLE, "value"),
            ],
        )
        def update_line_graph(
            range: str,
            type: str,
            edit_close_clicks: int,
            add_close_clicks: int,
            prev: int,
            next: int,
            edit_name: str,
            edit_rate: float,
            edit_start_date: str,
            edit_fixed_years: int,
            edit_fixed_months: int,
            edit_term_years: int,
            edit_term_months: int,
            edit_principle: float,
            add_name: str,
            add_rate: float,
            add_start_date: str,
            add_fixed_years: int,
            add_fixed_months: int,
            add_term_years: int,
            add_term_months: int,
            add_principle: float,
        ) -> tuple[html.Div, list[html.H4 | html.H6], list[html.H4 | html.H6]]:
            if ctx.triggered_id == ids.MORTGAGE_EDIT_MODAL_CLOSE:
                mortgage = self.selected_mortgage(next, prev)
                if edit_name:
                    mortgage.mortgage_name = edit_name
                if edit_rate:
                    mortgage.interest_rate = edit_rate / 100
                if edit_start_date:
                    mortgage.start_date = datetime.strptime(edit_start_date, "%Y-%m-%d")
                if edit_fixed_years or edit_fixed_months:
                    mortgage.fixed_term = (
                        (edit_fixed_years if edit_fixed_years else 0) * 12
                    ) + edit_fixed_months
                if edit_term_years or edit_term_months:
                    mortgage.term = (
                        (edit_term_years if edit_term_years else 0) * 12
                    ) + edit_term_months
                if edit_principle:
                    mortgage.principle_at_start = edit_principle

            if ctx.triggered_id == ids.MORTGAGE_ADD_MODAL_CLOSE:
                mortgage = MortgageAgreement(
                    start_year=datetime.strptime(add_start_date, "%Y-%m-%d").year,
                    start_month=datetime.strptime(add_start_date, "%Y-%m-%d").month,
                    mortgage_name=add_name,
                    interest_rate=int(add_rate) / 100,
                    term=((add_term_years if add_term_years else 0) * 12)
                    + add_term_months,
                    fixed_term=((add_fixed_years if add_fixed_years else 0) * 12)
                    + add_fixed_months,
                    principle_at_start=add_principle,
                )
                self.data.add_mortgage(mortgage=mortgage)

            record = self.data.payment_record  # will recalculate total record
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
            return (
                html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART),
                self.update_payment_text(range),
                self.update_interest_text(range),
            )

        # determines the text for the mortgage display modal
        @self.app.callback(
            Output(ids.MORTGAGE_AGREEMENT_MODAL_BODY, "children"),
            [
                Input(ids.MORTGAGE_AGREEMENT_MODAL_NEXT, "n_clicks"),
                Input(ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS, "n_clicks"),
            ],
        )
        def update_modal_text(next: int, prev: int) -> list[html.Div]:
            return [
                html.Div(line)
                for line in self.selected_mortgage(next, prev).display().split("\n")
            ]

        # disables next button when final mortgage is reached
        @self.app.callback(
            Output(ids.MORTGAGE_AGREEMENT_MODAL_NEXT, "disabled"),
            [
                Input(ids.MORTGAGE_AGREEMENT_MODAL_NEXT, "n_clicks"),
                Input(ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS, "n_clicks"),
            ],
        )
        def toggle_next(next: int, prev: int) -> bool:
            if next - prev >= len(self.data.mortgage_list) - 1:
                return True
            return False

        # fills in placeholders for the edit mortgage modal
        @self.app.callback(
            [
                Output(ids.MORTGAGE_EDIT_MODAL_NAME, "placeholder"),
                Output(ids.MORTGAGE_EDIT_MODAL_RATE, "placeholder"),
                Output(ids.MORTGAGE_EDIT_MODAL_START, "initial_visible_month"),
                Output(ids.MORTGAGE_EDIT_MODAL_START, "placeholder"),
                Output(ids.MORTGAGE_EDIT_MODAL_FIXED_TERM_YEARS, "placeholder"),
                Output(ids.MORTGAGE_EDIT_MODAL_FIXED_TERM_MOTHS, "placeholder"),
                Output(ids.MORTGAGE_EDIT_MODAL_TERM_YEARS, "placeholder"),
                Output(ids.MORTGAGE_EDIT_MODAL_TERM_MOTHS, "placeholder"),
                Output(ids.MORTGAGE_EDIT_MODAL_PRINCIPLE, "placeholder"),
            ],
            Input(ids.MORTGAGE_AGREEMENT_MODAL_EDIT, "n_clicks"),
            [
                State(ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS, "n_clicks"),
                State(ids.MORTGAGE_AGREEMENT_MODAL_NEXT, "n_clicks"),
            ],
        )
        def fill_placeholders(
            n1, prev, next
        ) -> tuple[str, str, date, str, int, int, int, int, str | None]:
            """gets the data from the currently displayed mortgage to fill all placeholders"""
            mortgage = self.selected_mortgage(next, prev)
            name = mortgage.mortgage_name
            rate = f"{mortgage.interest_rate * 100}%"
            start_date = mortgage.start_date
            fixed_years = floor(mortgage.fixed_term / 12)
            fixed_months = mortgage.fixed_term % 12
            term_years = floor(mortgage.term / 12)
            term_months = mortgage.term % 12
            principle = f"€{mortgage.principle_at_start:,.2f}"
            return (
                name,
                rate,
                start_date,
                start_date.strftime("%Y %b"),
                fixed_years,
                fixed_months,
                term_years,
                term_months,
                principle,
            )
