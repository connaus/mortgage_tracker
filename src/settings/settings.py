from dataclasses import dataclass


@dataclass
class Settings:

    mortgage_json: str = "src\\source_data\\mortgages.json"
    overpayment_file: str = r"C:\Users\ste-c\OneDrive\Documents\Mortgage\python_dashboard\src\source_data\overpayment_record.xlsx"
    currency_symbol: str = "€"
