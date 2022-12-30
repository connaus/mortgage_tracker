from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from . import ids
from datetime import date, datetime


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.MORTGAGE_EDIT_MODAL, "is_open"),
        [
            Input(ids.MORTGAGE_AGREEMENT_MODAL_EDIT, "n_clicks"),
            Input(ids.MORTGAGE_EDIT_MODAL_CLOSE, "n_clicks"),
        ],
        [State(ids.MORTGAGE_EDIT_MODAL, "is_open")],
    )
    def open_modal(n1, n2, is_open) -> bool:
        if n1 or n2:
            return not is_open
        return is_open

    return html.Div(
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Edit Mortgage")),
                dbc.ModalBody(
                    [
                        dbc.Label("Mortgage Name:"),
                        dbc.Input(
                            id=ids.MORTGAGE_EDIT_MODAL_NAME, type="text", debounce=True
                        ),
                        dbc.Label("Interest Rate (in percentage):"),
                        dbc.Input(
                            id=ids.MORTGAGE_EDIT_MODAL_RATE,
                            type="number",
                            debounce=True,
                            min=0,
                        ),
                        dbc.Label("Start Date:"),
                        dcc.DatePickerSingle(
                            id=ids.MORTGAGE_EDIT_MODAL_START,
                            initial_visible_month=date(
                                year=2022, month=12, day=1
                            ),  # datetime.today().date,
                        ),
                        dbc.Label("Fixed Term:"),
                        dbc.Label("Years"),
                        dbc.Input(
                            id=ids.MORTGAGE_EDIT_MODAL_FIXED_TERM_YEARS,
                            type="number",
                            min=0,
                        ),
                        dbc.Label("Months"),
                        dbc.Input(
                            id=ids.MORTGAGE_EDIT_MODAL_FIXED_TERM_MOTHS,
                            type="number",
                            min=0,
                            max=12,
                        ),
                        dbc.Label("Total Term:"),
                        dbc.Label("Years"),
                        dbc.Input(
                            id=ids.MORTGAGE_EDIT_MODAL_TERM_YEARS,
                            type="number",
                            min=0,
                        ),
                        dbc.Label("Months"),
                        dbc.Input(
                            id=ids.MORTGAGE_EDIT_MODAL_TERM_MOTHS,
                            type="number",
                            min=0,
                            max=12,
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Save and Close",
                        id=ids.MORTGAGE_EDIT_MODAL_CLOSE,
                        class_name="ms-auto",
                        n_clicks=0,
                    ),
                ),
            ],
            id=ids.MORTGAGE_EDIT_MODAL,
            is_open=False,
        )
    )
