from src.components.layout import create_layout
from src.mortgage_data import TotalPaymentRecord, PaymentSchema
import plotly.express as px
from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP


def main():

    m = TotalPaymentRecord()
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Mortgage Tracker"
    app.layout = create_layout(app, m)
    app.run()

    """m = TotalPaymentRecord()
    mortgage = m.calculate_payments()

    fig = px.line(
        x=mortgage.index,
        y=mortgage[PaymentSchema.principle_at_start],
        markers=True,
        title=PaymentSchema.principle_at_start,
        color=mortgage[PaymentSchema.mortgage_name],
    )
    fig.show()"""


if __name__ == "__main__":
    main()
