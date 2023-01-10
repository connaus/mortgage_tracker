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
        output.append(html.Div(f'{idx.strftime("%Y %B")}\t€{payment:,.2f}'))

    return output


def render(updater: Updater, style: dict = {}) -> html.Div:
    @updater.app.callback(
        Output(ids.OVERPAYMENT_MODAL, "is_open"),
        Input(ids.OVERPAYMENT_MODAL_OPEN, "n_clicks"),
        [State(ids.OVERPAYMENT_MODAL, "is_open")],
    )
    def toggle_modal(n1, is_open) -> bool:
        if n1:
            return not is_open
        return is_open

    return html.Div(
        children=html.Div(
            [
                dbc.Button(
                    "View/Edit Overpayments",
                    id=ids.OVERPAYMENT_MODAL_OPEN,
                    n_clicks=0,
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Overpayments")),
                        dbc.ModalBody(build_overpayment_text(updater=updater)),
                    ],
                    id=ids.OVERPAYMENT_MODAL,
                    is_open=False,
                ),
            ]
        ),
        style=style,
    )
