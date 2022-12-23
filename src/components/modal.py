from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from . import ids
from ..mortgage_data import MortgageAgreement


def modal_children(i: int, mortgage_list: list[MortgageAgreement]) -> html.Div:
    print("resetting modal")
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
                    dbc.ModalBody(
                        mortgage_list[i].__repr__(),
                        id=ids.MORTGAGE_AGREEMENT_MODAL_BODY,
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Previous",
                                id=ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS,
                                class_name="ms-auto",
                                n_clicks=0,
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
                            ),
                        ]
                    ),
                ],
                id=ids.MORTGAGE_AGREEMENT_MODAL,
                is_open=False,
                style={"width": "25%", "display": "inline-block"},
            ),
        ]
    )


def render(app: Dash, mortgage_list: list[MortgageAgreement]) -> html.Div:
    @app.callback(
        Output(ids.MORTGAGE_AGREEMENT_MODAL, "is_open"),
        Input(ids.MORTGAGE_AGREEMENT_MODAL_OPEN, "n_clicks"),
        # Input(ids.MORTGAGE_AGREEMENT_MODAL_CLOSE, "n_clicks"),
        [State(ids.MORTGAGE_AGREEMENT_MODAL, "is_open")],
    )
    def toggle_modal(n1, is_open) -> bool:
        print("I should open up more")
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
    def update_modal_text(n1: int, n2: int) -> str:
        return mortgage_list[n1 - n2].__repr__()

    return html.Div(className="modalCentre", children=modal_children(0, mortgage_list))
