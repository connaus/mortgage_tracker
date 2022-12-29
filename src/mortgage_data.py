from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Optional
import pandas as pd
import numpy_financial as npf
from dateutil.relativedelta import relativedelta

OVERPAYMENT_FILE = Path(
    r"C:\Users\ste-c\OneDrive\Documents\Mortgage\python_dashboard\source_data\overpayment_record.xlsx"
)
MORTGAGE_DATA = Path("source_data\\mortgages.json")


def months_difference(start_date: datetime, end_date: datetime) -> int:
    return (
        (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
    ) + 1


class PaymentSchema:

    principle_at_start = "Principle At Start"
    interest_owed = "Interest Owed"
    payment_owed = "Payment Owed"
    actual_payment = "Actual Payment"
    principle_at_end = "Principle At End"
    mortgage_name = "Mortgage Name"
    overpayment = "Overpayment"


def overpayment_series() -> pd.Series:
    df = pd.read_excel(OVERPAYMENT_FILE)

    df["Month"] = df["Month"].apply(lambda x: x.to_pydatetime())
    df["Month"] = df["Month"].apply(lambda x: x.replace(day=1))

    df = df.set_index("Month")

    return df[PaymentSchema.overpayment]


@dataclass(order=True)
class MortgageAgreement:
    """class to store the details of mortgages"""

    start_year: int
    start_month: int
    mortgage_name: str
    interest_rate: float
    term: int  # in months
    fixed_term: int  # in months
    principle_at_start: Optional[float] = None

    def __post_init__(self) -> None:
        """calculate the months repayments here"""
        self.start_date = datetime(year=self.start_year, month=self.start_month, day=1)
        self.end_date = self.start_date + relativedelta(months=self.term - 1)
        self.fixed_term_end = self.start_date + relativedelta(
            months=self.fixed_term - 1
        )


def monthly_repayment(
    mortgage: MortgageAgreement, principle: float, date: datetime
) -> float:
    """returns the monthly repayment for a given mortgage"""
    months_remaining = months_difference(date, mortgage.end_date)
    return -1 * round(
        float(npf.pmt(mortgage.interest_rate / 12, months_remaining, principle)),
        2,
    )


class MortgagePaymentRecord:
    """payment record for a specific mortgage."""

    def __init__(self, mortgage: MortgageAgreement) -> None:
        self.mortgage = mortgage
        self._payment_df = pd.DataFrame(
            index=[
                mortgage.start_date + relativedelta(months=i)
                for i in range(mortgage.fixed_term)
            ],
        )

    @property
    def payment_df(self) -> pd.DataFrame:
        """dataframe containing all of the information about actual payments"""
        if not self.mortgage.principle_at_start:
            return (
                self._payment_df
            )  # return empty dataframe if initial principle unknown

        # add overpayment data
        ser = overpayment_series()
        self._payment_df = self._payment_df.join(ser, how="left")
        self._payment_df[PaymentSchema.overpayment] = self._payment_df[
            PaymentSchema.overpayment
        ].fillna(0)

        # calculate the payments
        self.add_actual_payment()
        self._payment_df[PaymentSchema.mortgage_name] = self.mortgage.mortgage_name

        return self._payment_df

    def add_actual_payment(self) -> None:
        """calcuates each months payment information, one row at a time."""
        # running_principle = self._payment_df.iloc[0][PaymentSchema.principle_at_start]
        if self.mortgage.principle_at_start:
            running_principle = self.mortgage.principle_at_start
            for idx in self._payment_df.index:
                self._payment_df.at[
                    idx, PaymentSchema.principle_at_start
                ] = running_principle
                self._payment_df.at[idx, PaymentSchema.interest_owed] = (
                    running_principle * self.mortgage.interest_rate / 12
                )
                self._payment_df.at[
                    idx, PaymentSchema.payment_owed
                ] = monthly_repayment(self.mortgage, running_principle, idx)
                self._payment_df.at[idx, PaymentSchema.actual_payment] = (
                    self._payment_df.at[idx, PaymentSchema.payment_owed]
                    + self._payment_df.at[idx, PaymentSchema.overpayment]
                )
                running_principle = (
                    running_principle
                    + self._payment_df.at[idx, PaymentSchema.interest_owed]
                    - self._payment_df.at[idx, PaymentSchema.actual_payment]
                )
                self._payment_df.at[
                    idx, PaymentSchema.principle_at_end
                ] = running_principle


class TotalPaymentRecord:
    """class to gather all information about the payments. stores the list of existing mortgages,
    as well as the payment record"""

    def __init__(self) -> None:
        with open(MORTGAGE_DATA) as f:
            mortgage_data_list = json.load(f)
        self.mortgage_list = [MortgageAgreement(**i) for i in mortgage_data_list]
        self.mortgage_list.sort()
        future_mortgage = self.calculate_future_mortgage()
        self.mortgage_list.append(future_mortgage)
        self.payment_record = self.calculate_payment_record()

    def calculate_future_mortgage(self) -> MortgageAgreement:
        """extends the last mortgage out to the remaining term to allow projections"""
        return MortgageAgreement(
            start_year=(
                self.mortgage_list[-1].fixed_term_end + relativedelta(months=1)
            ).year,
            start_month=(
                self.mortgage_list[-1].fixed_term_end + relativedelta(months=1)
            ).month,
            mortgage_name="Future",
            interest_rate=self.mortgage_list[-1].interest_rate,
            term=self.mortgage_list[-1].term - self.mortgage_list[-1].fixed_term,
            fixed_term=self.mortgage_list[-1].term - self.mortgage_list[-1].fixed_term,
        )

    def calculate_payment_record(self) -> pd.DataFrame:
        record_list: list[pd.DataFrame] = list()
        for i, mortgage in enumerate(self.mortgage_list):
            if not mortgage.principle_at_start and i != 0:
                mortgage.principle_at_start = record_list[i - 1].iloc[-1][
                    PaymentSchema.principle_at_end
                ]
            record_list.append(MortgagePaymentRecord(mortgage).payment_df)
        return pd.concat(record_list)

    def record_to_date(self) -> pd.DataFrame:
        """record up to and including current month"""
        return self.payment_record[self.payment_record.index < datetime.today()]

    def record_agreed(self) -> pd.DataFrame:
        """record only for months with a mortgage agreement in place"""
        return self.payment_record[
            self.payment_record[PaymentSchema.mortgage_name] != "Future"
        ]

    def total_interest_payment_to_date(self) -> float:
        """returns the total amount paid including current month"""
        df = self.payment_record[self.payment_record.index < datetime.today()]
        return df[PaymentSchema.interest_owed].sum()

    def perc_interest_payment_to_date(self) -> float:
        """calculate percentage of payment to date that has gone to interest"""
        return self.total_interest_payment_to_date() / self.payment_to_date()

    def payment_to_date(self) -> float:
        """returns the total amount paid including current month"""
        df = self.record_to_date()
        return df[PaymentSchema.actual_payment].sum()

    def principle_reduction_to_date(self) -> float:
        """principle reduction form initial mortgage to current month (after payment)"""
        df = self.record_to_date()
        return (
            df[PaymentSchema.principle_at_start][0]
            - df[PaymentSchema.principle_at_end][-1]
        )

    def payment_agreed(self) -> float:
        """total paid, including overpayments, until end of final mortgage agreement"""
        df = self.record_agreed()
        return df[PaymentSchema.actual_payment].sum()

    def principle_reduction_agreed(self) -> float:
        """principle reduction form initial mortgage to end of final mortgage agreement"""
        df = self.record_agreed()
        return (
            df[PaymentSchema.principle_at_start][0]
            - df[PaymentSchema.principle_at_end][-1]
        )

    def cost_of_mortgage(self) -> float:
        """total paid until principle is 0"""
        return self.payment_record[PaymentSchema.actual_payment].sum()

    def perc_mortgage_paid(self) -> float:
        """perc of cost of mortgage already paid"""
        return self.payment_to_date() / self.cost_of_mortgage()
