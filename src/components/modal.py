from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from . import ids
from ..mortgage_data import MortgageAgreement


def render(app: Dash, mortgage_list: list[MortgageAgreement]) -> html.Div:
    @app.callback(
        Output(ids.MORTGAGE_AGREEMENT_MODAL, "is_open"),
        Input(ids.MORTGAGE_AGREEMENT_MODAL_OPEN, "n_clicks"),
        [State(ids.MORTGAGE_AGREEMENT_MODAL, "is_open")],
    )
    def toggle_modal(n1, is_open) -> bool:
        if n1:
            return not is_open
        return is_open

    @app.callback(
        Output(ids.MORTGAGE_AGREEMENT_MODAL_BODY, "children"),
        [
            Input(ids.MORTGAGE_AGREEMENT_MODAL_NEXT, "n_clicks"),
            Input(ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS, "n_clicks"),
        ],
    )
    def update_modal_text(next: int, prev: int) -> str:
        return mortgage_list[next - prev].__repr__()

    @app.callback(
        Output(ids.MORTGAGE_AGREEMENT_MODAL_NEXT, "disabled"),
        [
            Input(ids.MORTGAGE_AGREEMENT_MODAL_NEXT, "n_clicks"),
            Input(ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS, "n_clicks"),
        ],
    )
    def toggle_next(next: int, prev: int) -> bool:
        if (
            next - prev >= len(mortgage_list) - 2
        ):  # -2 as we want to exclude "Future" agreement
            return True
        return False

    @app.callback(
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
                            mortgage_list[0].__repr__(),
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
        style={"width": "25%", "display": "inline-block"},
    )
