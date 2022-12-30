from src.components.layout import create_layout
from src.mortgage_data import TotalPaymentRecord, PaymentSchema
import plotly.express as px
from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP


def main():

    data = TotalPaymentRecord()
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Mortgage Tracker"
    app.layout = create_layout(app, data)
    app.run()


if __name__ == "__main__":
    main()
