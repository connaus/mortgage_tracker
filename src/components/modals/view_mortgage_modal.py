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
                    "View/Edit Mortgages",
                    id=ids.MORTGAGE_AGREEMENT_MODAL_OPEN,
                    n_clicks=0,
                    style={"width": "100%"},
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
                                    n_clicks=0,
                                    disabled=True,
                                    style={"flex": 1},
                                ),
                                dbc.Button(
                                    "New",
                                    id=ids.MORTGAGE_ADD_MODAL_OPEN,
                                    n_clicks=0,
                                    style={"flex": 1},
                                ),
                                dbc.Button(
                                    "Edit",
                                    id=ids.MORTGAGE_AGREEMENT_MODAL_EDIT,
                                    n_clicks=0,
                                    style={"flex": 1},
                                ),
                                dbc.Button(
                                    "Delete",
                                    id=ids.MORTGAGE_AGREEMENT_MODAL_DELETE,
                                    n_clicks=0,
                                    style={"flex": 1},
                                ),
                                dbc.Button(
                                    "Next",
                                    id=ids.MORTGAGE_AGREEMENT_MODAL_NEXT,
                                    n_clicks=0,
                                    disabled=False,
                                    style={"flex": 1},
                                ),
                            ],
                            style={"display": "flex"},
                        ),
                    ],
                    id=ids.MORTGAGE_AGREEMENT_MODAL,
                    is_open=False,
                ),
            ],
        ),
        style=style,
    )
