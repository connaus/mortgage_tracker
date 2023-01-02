from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from .. import ids
from datetime import date


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
        """opens modal when the edit button on the view mortgage modal is clicked
        closes it when save and close is clicked"""
        if n1 or n2:
            return not is_open
        return is_open

    return html.Div(
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Edit Mortgage")),
                dbc.ModalBody(
                    [
                        html.Div(
                            [
                                dbc.Label("Mortgage Name:"),
                                dbc.Input(
                                    id=ids.MORTGAGE_EDIT_MODAL_NAME,
                                    type="text",
                                    debounce=True,
                                ),
                                dbc.Label("Interest Rate (in percentage):"),
                                dbc.Input(
                                    id=ids.MORTGAGE_EDIT_MODAL_RATE,
                                    type="number",
                                    debounce=True,
                                    min=0,
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Label("Start Date:", style={"flex": 1}),
                                dcc.DatePickerSingle(
                                    id=ids.MORTGAGE_EDIT_MODAL_START,
                                    initial_visible_month=date.today(),
                                    style={"flex": 1},
                                ),
                            ],
                            style={"display": "flex"},
                        ),
                        html.Div(
                            [
                                dbc.Label("Fixed Term:"),
                                html.Div(
                                    [
                                        dbc.Label("Years", style={"flex": 1}),
                                        dbc.Label("Months", style={"flex": 1}),
                                    ],
                                    style={"display": "flex"},
                                ),
                                html.Div(
                                    [
                                        dbc.Input(
                                            id=ids.MORTGAGE_EDIT_MODAL_FIXED_TERM_YEARS,
                                            type="number",
                                            min=0,
                                            debounce=True,
                                            style={"flex": 1},
                                        ),
                                        dbc.Input(
                                            id=ids.MORTGAGE_EDIT_MODAL_FIXED_TERM_MOTHS,
                                            type="number",
                                            min=0,
                                            max=12,
                                            debounce=True,
                                            style={"flex": 1},
                                        ),
                                    ],
                                    style={"display": "flex"},
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Label("Total Term:"),
                                html.Div(
                                    [
                                        dbc.Label(
                                            "Years",
                                            style={"flex": 1},
                                        ),
                                        dbc.Label(
                                            "Months",
                                            style={"flex": 1},
                                        ),
                                    ],
                                    style={"display": "flex"},
                                ),
                                html.Div(
                                    [
                                        dbc.Input(
                                            id=ids.MORTGAGE_EDIT_MODAL_TERM_YEARS,
                                            type="number",
                                            min=0,
                                            debounce=True,
                                            style={"flex": 1},
                                        ),
                                        dbc.Input(
                                            id=ids.MORTGAGE_EDIT_MODAL_TERM_MOTHS,
                                            type="number",
                                            min=0,
                                            max=12,
                                            debounce=True,
                                            style={"flex": 1},
                                        ),
                                    ],
                                    style={"display": "flex"},
                                ),
                            ]
                        ),
                        dbc.Label("Starting Principle:"),
                        dbc.Input(
                            id=ids.MORTGAGE_EDIT_MODAL_PRINCIPLE,
                            type="number",
                            debounce=True,
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
