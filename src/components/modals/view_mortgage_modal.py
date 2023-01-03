from dash import html, Output, Input, State
import dash_bootstrap_components as dbc
from .. import ids
from processor.model_view_link import Updater


def render(updater: Updater, style: dict = {}) -> html.Div:
    @updater.app.callback(
        Output(ids.MORTGAGE_AGREEMENT_MODAL, "is_open"),
        Input(ids.MORTGAGE_AGREEMENT_MODAL_OPEN, "n_clicks"),
        [State(ids.MORTGAGE_AGREEMENT_MODAL, "is_open")],
    )
    def toggle_modal(n1, is_open) -> bool:
        if n1:
            return not is_open
        return is_open

    @updater.app.callback(
        Output(ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS, "disabled"),
        [
            Input(ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS, "n_clicks"),
            Input(ids.MORTGAGE_AGREEMENT_MODAL_NEXT, "n_clicks"),
        ],
    )
    def toggle_prev(prev: int, next: int) -> bool:
        if next - prev <= 0:
            return True
        return False

    return html.Div(
        children=html.Div(
            [
                dbc.Button(
                    "Open Mortgage Details",
                    id=ids.MORTGAGE_AGREEMENT_MODAL_OPEN,
                    n_clicks=0,
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Mortgage Details")),
                        dbc.ModalBody(
                            [html.Div()],
                            id=ids.MORTGAGE_AGREEMENT_MODAL_BODY,
                        ),
                        dbc.ModalFooter(
                            [
                                dbc.Button(
                                    "Previous",
                                    id=ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS,
                                    class_name="ms-auto",
                                    n_clicks=0,
                                    disabled=True,
                                ),
                                dbc.Button(
                                    "Edit",
                                    id=ids.MORTGAGE_AGREEMENT_MODAL_EDIT,
                                    class_name="ms-auto",
                                    n_clicks=0,
                                ),
                                dbc.Button(
                                    "Next",
                                    id=ids.MORTGAGE_AGREEMENT_MODAL_NEXT,
                                    class_name="ms-auto",
                                    n_clicks=0,
                                    disabled=False,
                                ),
                            ]
                        ),
                    ],
                    id=ids.MORTGAGE_AGREEMENT_MODAL,
                    is_open=False,
                ),
            ],
        ),
        style={"width": "25%", "display": "inline-block", "verticalAlign": "bottom"},
    )
