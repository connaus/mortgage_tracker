from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from . import ids
from ..mortgage_data import MortgageAgreement

i = 0


def render(app: Dash, mortgage_list: list[MortgageAgreement]) -> html.Div:
    @app.callback(
        Output(ids.MORTGAGE_AGREEMENT_MODAL, "is_open"),
        [
            Input(ids.MORTGAGE_AGREEMENT_MODAL_OPEN, "n_clicks"),
            # Input(ids.MORTGAGE_AGREEMENT_MODAL_CLOSE, "n_clicks"),
        ],
        [State(ids.MORTGAGE_AGREEMENT_MODAL, "is_open")],
    )
    def toggle_modal(n1, is_open) -> bool:
        if n1:
            return not is_open
        return is_open

    return html.Div(
        [
            dbc.Button(
                "Open Mortgage Details",
                id=ids.MORTGAGE_AGREEMENT_MODAL_OPEN,
                n_clicks=0,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Mortgage Details")),
                    dbc.ModalBody(mortgage_list[i].__repr__()),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Close",
                                id=ids.MORTGAGE_AGREEMENT_MODAL_CLOSE,
                                class_name="ms-auto",
                                n_clicks=0,
                            ),
                            # dbc.Button(
                            #     "Next",
                            #     id=ids.MORTGAGE_AGREEMENT_MODAL_NEXT,
                            #     class_name="ms-auto",
                            #     n_clicks=0,
                            # ),
                        ]
                    ),
                ],
                id=ids.MORTGAGE_AGREEMENT_MODAL,
                is_open=False,
                style={"width": "25%", "display": "inline-block"},
            ),
        ]
    )
