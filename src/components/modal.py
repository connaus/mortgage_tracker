from dash import Dash, html, Output, Input, State, dcc
from datetime import datetime, date
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
    def update_modal_text(next: int, prev: int) -> list[html.Div]:
        return [
            html.Div(line) for line in mortgage_list[next - prev].display().split("\n")
        ]

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

    # edit modal callbacks
    @app.callback(
        Output(ids.MORTGAGE_EDIT_MODAL, "is_open"),
        [
            Input(ids.MORTGAGE_AGREEMENT_MODAL_EDIT, "n_clicks"),
            Input(ids.MORTGAGE_EDIT_MODAL_CLOSE, "n_clicks"),
        ],
        [State(ids.MORTGAGE_EDIT_MODAL, "is_open")],
    )
    def open_modal(n1, n2, is_open) -> bool:
        if n1 or n2:
            return not is_open
        return is_open

    # @app.callback(
    #     Output(ids.MORTGAGE_EDIT_MODAL, "is_open"),
    #     Input(ids.MORTGAGE_EDIT_MODAL_CLOSE, "n_clicks"),
    #     [State(ids.MORTGAGE_EDIT_MODAL, "is_open")],
    # )
    # def close_modal(n1, is_open) -> bool:
    #     if n1:
    #         return not is_open
    #     return is_open

    view_mortgage = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Mortgage Details")),
            dbc.ModalBody(
                [html.Div(line) for line in mortgage_list[0].display().split("\n")],
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
    )

    edit_mortgage = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Edit Mortgage")),
            dbc.ModalBody(
                [
                    dbc.Label("Mortgage Name:"),
                    dbc.Input(
                        id=ids.MORTGAGE_EDIT_MODAL_NAME, type="text", debounce=True
                    ),
                    dbc.Label("Interest Rate (in percentage):"),
                    dbc.Input(
                        id=ids.MORTGAGE_EDIT_MODAL_RATE,
                        type="number",
                        debounce=True,
                        min=0,
                    ),
                    dbc.Label("Start Date:"),
                    dcc.DatePickerSingle(
                        id=ids.MORTGAGE_EDIT_MODAL_START,
                        initial_visible_month=date(
                            year=2022, month=12, day=1
                        ),  # datetime.today().date,
                    ),
                    dbc.Label("Fixed Term:"),
                    dbc.Label("Years"),
                    dbc.Input(
                        id=ids.MORTGAGE_EDIT_MODAL_FIXED_TERM_YEARS,
                        type="number",
                        min=0,
                    ),
                    dbc.Label("Months"),
                    dbc.Input(
                        id=ids.MORTGAGE_EDIT_MODAL_FIXED_TERM_MOTHS,
                        type="number",
                        min=0,
                        max=12,
                    ),
                    dbc.Label("Total Term:"),
                    dbc.Label("Years"),
                    dbc.Input(
                        id=ids.MORTGAGE_EDIT_MODAL_TERM_YEARS,
                        type="number",
                        min=0,
                    ),
                    dbc.Label("Months"),
                    dbc.Input(
                        id=ids.MORTGAGE_EDIT_MODAL_TERM_MOTHS,
                        type="number",
                        min=0,
                        max=12,
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

    return html.Div(
        children=html.Div(
            [
                dbc.Button(
                    "Open Mortgage Details",
                    id=ids.MORTGAGE_AGREEMENT_MODAL_OPEN,
                    n_clicks=0,
                ),
                view_mortgage,
                edit_mortgage,
                # dbc.Modal(
                #     [
                #         dbc.ModalHeader(dbc.ModalTitle("Mortgage Details")),
                #         dbc.ModalBody(
                #             [
                #                 html.Div(line)
                #                 for line in mortgage_list[0].display().split("\n")
                #             ],
                #             id=ids.MORTGAGE_AGREEMENT_MODAL_BODY,
                #         ),
                #         dbc.ModalFooter(
                #             [
                #                 dbc.Button(
                #                     "Previous",
                #                     id=ids.MORTGAGE_AGREEMENT_MODAL_PREVIOUS,
                #                     class_name="ms-auto",
                #                     n_clicks=0,
                #                     disabled=True,
                #                 ),
                #                 dbc.Button(
                #                     "Edit",
                #                     id=ids.MORTGAGE_AGREEMENT_MODAL_EDIT,
                #                     class_name="ms-auto",
                #                     n_clicks=0,
                #                 ),
                #                 dbc.Button(
                #                     "Next",
                #                     id=ids.MORTGAGE_AGREEMENT_MODAL_NEXT,
                #                     class_name="ms-auto",
                #                     n_clicks=0,
                #                     disabled=False,
                #                 ),
                #             ]
                #         ),
                #     ],
                #     id=ids.MORTGAGE_AGREEMENT_MODAL,
                #     is_open=False,
                # ),
            ],
        ),
        style={"width": "25%", "display": "inline-block"},
    )
