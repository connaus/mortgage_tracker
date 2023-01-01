from components.layout import create_layout
from data.mortgage_data import TotalPaymentRecord
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP


def main():

    data = TotalPaymentRecord()
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Mortgage Tracker"
    app.layout = create_layout(app, data)
    app.run()


if __name__ == "__main__":
    main()
