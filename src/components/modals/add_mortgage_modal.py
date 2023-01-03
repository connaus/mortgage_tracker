from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from .. import ids
from dateutil.relativedelta import relativedelta
from processor.model_view_link import Updater


def render(updater: Updater, style: dict = {}) -> html.Div:
    @updater.app.callback(
        Output(ids.MORTGAGE_ADD_MODAL, "is_open"),
        [
            Input(ids.MORTGAGE_ADD_MODAL_OPEN, "n_clicks"),
            Input(ids.MORTGAGE_ADD_MODAL_CLOSE, "n_clicks"),
        ],
        [State(ids.MORTGAGE_ADD_MODAL, "is_open")],
    )
    def open_modal(n1, n2, is_open) -> bool:
        """opens modal when the edit button on the view mortgage modal is clicked
        closes it when save and close is clicked"""
        if n1 or n2:
            return not is_open
        return is_open

    return html.Div(
        children=html.Div(
            [
                dbc.Button(
                    "Add New Mortgage",
                    id=ids.MORTGAGE_ADD_MODAL_OPEN,
                    n_clicks=0,
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Add Mortgage")),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Mortgage Name:"),
                                        dbc.Input(
                                            id=ids.MORTGAGE_ADD_MODAL_NAME,
                                            type="text",
                                            debounce=True,
                                            required=True,
                                        ),
                                        dbc.Label("Interest Rate (in percentage):"),
                                        dbc.Input(
                                            id=ids.MORTGAGE_ADD_MODAL_RATE,
                                            type="number",
                                            debounce=True,
                                            required=True,
                                            min=0,
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Start Date:", style={"flex": 1}),
                                        dcc.DatePickerSingle(
                                            id=ids.MORTGAGE_ADD_MODAL_START,
                                            date=updater.data.mortgage_list[
                                                -1
                                            ].fixed_term_end
                                            + relativedelta(months=1),
                                            style={"flex": 1},
                                            number_of_months_shown=3,
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
                                                    id=ids.MORTGAGE_ADD_MODAL_FIXED_TERM_YEARS,
                                                    type="number",
                                                    min=0,
                                                    debounce=True,
                                                    required=True,
                                                    style={"flex": 1},
                                                ),
                                                dbc.Input(
                                                    id=ids.MORTGAGE_ADD_MODAL_FIXED_TERM_MOTHS,
                                                    type="number",
                                                    min=0,
                                                    max=12,
                                                    debounce=True,
                                                    required=True,
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
                                                    id=ids.MORTGAGE_ADD_MODAL_TERM_YEARS,
                                                    type="number",
                                                    min=0,
                                                    debounce=True,
                                                    required=True,
                                                    style={"flex": 1},
                                                ),
                                                dbc.Input(
                                                    id=ids.MORTGAGE_ADD_MODAL_TERM_MOTHS,
                                                    type="number",
                                                    min=0,
                                                    max=12,
                                                    debounce=True,
                                                    required=True,
                                                    style={"flex": 1},
                                                ),
                                            ],
                                            style={"display": "flex"},
                                        ),
                                    ]
                                ),
                                dbc.Label("Starting Principle:"),
                                dbc.Input(
                                    id=ids.MORTGAGE_ADD_MODAL_PRINCIPLE,
                                    type="number",
                                    debounce=True,
                                ),
                            ]
                        ),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Save and Close",
                                id=ids.MORTGAGE_ADD_MODAL_CLOSE,
                                class_name="ms-auto",
                                n_clicks=0,
                            ),
                        ),
                    ],
                    id=ids.MORTGAGE_ADD_MODAL,
                    is_open=False if updater.data.mortgage_list else True,
                ),
            ]
        ),
        style=style,
    )
