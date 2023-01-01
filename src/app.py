from components.layout import create_layout
from data.mortgage_data import TotalPaymentRecord
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from processor.model_view_link import Updater


def main():

    data = TotalPaymentRecord()
    app = Dash(external_stylesheets=[BOOTSTRAP])
    p = Updater(app, data)
    p.run()
    app.title = "Mortgage Tracker"
    app.layout = create_layout(app, data)
    app.run(debug=True)


if __name__ == "__main__":
    main()
