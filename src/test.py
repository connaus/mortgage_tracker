from data.mortgage_data import TotalPaymentRecord
import json
from settings.settings import Settings

with open("src\\settings\\settings.json") as f:
    settings = json.load(f)
s = Settings(**settings)

t = TotalPaymentRecord(settings=s)

ser = t.overpayment_series
ser = ser.dropna()
ser = ser[ser != 0]
for idx, i in ser.items():
    print(f'{idx.strftime("%Y %B")}\t€{i:,.2f}')
