from dash import html, Output, Input, State
import dash_bootstrap_components as dbc
from .. import ids
from processor.model_view_link import Updater


def build_overpayment_text(updater: Updater) -> list[html.Div]:

    overpayments = updater.data.overpayment_series
    overpayments = overpayments.dropna()
    overpayments = overpayments[overpayments != 0]
    output = []
    for idx, payment in overpayments.items():
        output.append(
            html.Div(
                [
                    html.Div(
                        f'{idx.strftime("%Y %B")}:',
                        style={"flex": 1, "text-align": "right"},
                    ),
                    html.Div(style={"flex": 0.5}),
                    html.Div(
                        f"€{payment:,.2f}",
                        style={"flex": 1, "text-align": "left"},
                    ),
                ],
                style={"display": "flex"},
            )
        )

    output.reverse()
    return output


def render(updater: Updater, style: dict = {}) -> html.Div:
    @updater.app.callback(
        Output(ids.OVERPAYMENT_MODAL, "is_open"),
        [
            Input(ids.OVERPAYMENT_MODAL_OPEN, "n_clicks"),
            Input(ids.OVERPAYMENT_MODAL_CLOSE, "n_clicks"),
        ],
        [State(ids.OVERPAYMENT_MODAL, "is_open")],
    )
    def toggle_modal(n1, n2, is_open) -> bool:
        if n1 or n2:
            return not is_open
        return is_open

    @updater.app.callback(
        Output(ids.OVERPAYMENT_MODAL_BODY, "children"),
        [
            Input(ids.OVERPAYMENT_MODAL_OPEN, "n_clicks"),
            Input(ids.ADD_OVERPAYMENT_MODAL_CLOSE, "n_clicks"),
        ],
    )
    def update_modal_text(n1, n2) -> list[html.Div]:
        return build_overpayment_text(updater=updater)

    return html.Div(
        children=html.Div(
            [
                dbc.Button(
                    "View/Edit Overpayments",
                    id=ids.OVERPAYMENT_MODAL_OPEN,
                    n_clicks=0,
                    style={"width": "100%"},
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Overpayments")),
                        dbc.ModalBody(
                            build_overpayment_text(updater=updater),
                            id=ids.OVERPAYMENT_MODAL_BODY,
                        ),
                        dbc.ModalFooter(
                            [
                                dbc.Button(
                                    "Add/Edit Entry",
                                    id=ids.OVERPAYMENT_MODAL_ADD,
                                    n_clicks=0,
                                    style={"flex": 1},
                                ),
                                dbc.Button(
                                    "Close",
                                    id=ids.OVERPAYMENT_MODAL_CLOSE,
                                    n_clicks=0,
                                    style={"flex": 1},
                                ),
                            ],
                            style={"display": "flex"},
                        ),
                    ],
                    id=ids.OVERPAYMENT_MODAL,
                    is_open=False,
                    scrollable=True,
                ),
            ]
        ),
        style=style,
    )
