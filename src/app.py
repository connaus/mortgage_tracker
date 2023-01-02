import json
from components.layout import create_layout
from data.mortgage_data import TotalPaymentRecord
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from processor.model_view_link import Updater
from settings.settings import Settings


def main():

    with open("src\\settings\\settings.json") as f:
        settings = json.load(f)
    s = Settings(**settings)
    data = TotalPaymentRecord(s)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    updater = Updater(app, data)
    updater.run()
    app.title = "Mortgage Tracker"
    app.layout = create_layout(updater)
    app.run(debug=True)


if __name__ == "__main__":
    main()
