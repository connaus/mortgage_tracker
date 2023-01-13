from datetime import date
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from .. import ids
from processor.model_view_link import Updater


def render(updater: Updater, style: dict = {}) -> dbc.Modal:
    @updater.app.callback(
        Output(ids.ADD_OVERPAYMENT_MODAL, "is_open"),
        [
            Input(ids.OVERPAYMENT_MODAL_ADD, "n_clicks"),
            Input(ids.ADD_OVERPAYMENT_MODAL_CLOSE, "n_clicks"),
        ],
        [State(ids.ADD_OVERPAYMENT_MODAL, "is_open")],
    )
    def open_modal(n1, n2, is_open) -> bool:
        """opens modal when the edit button on the view mortgage modal is clicked
        closes it when save and close is clicked"""
        if n1 or n2:
            return not is_open
        return is_open

    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Add Overpayment")),
            dbc.ModalBody(
                [
                    html.Div(dbc.Label("Date:")),
                    html.Div(
                        dcc.DatePickerSingle(
                            id=ids.ADD_OVERPAYMENT_MODAL_DATE,
                            date=date.today(),
                            style={"flex": 1},
                            number_of_months_shown=3,
                            display_format="MMM YYYY",
                        ),
                    ),
                    html.Div(dbc.Label("Overpayment Amount:")),
                    html.Div(
                        dbc.Input(
                            id=ids.ADD_OVERPAYMENT_MODAL_AMOUNT,
                            type="number",
                            debounce=True,
                            required=True,
                            style={"flex": 1},
                        )
                    ),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Save and Close",
                    id=ids.ADD_OVERPAYMENT_MODAL_CLOSE,
                    class_name="ms-auto",
                    n_clicks=0,
                ),
            ),
        ],
        id=ids.ADD_OVERPAYMENT_MODAL,
        is_open=False,
    )
